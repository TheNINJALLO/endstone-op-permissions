"""
OP Permissions Plugin for Endstone

Provides permissions for structure blocks and command blocks without requiring OP status.
"""

import json
from pathlib import Path
from typing import Dict, Any

from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerJoinEvent, PlayerQuitEvent
from endstone.command import Command, CommandSender
from typing import Set


class OpPermissionsPlugin(Plugin):
    """Main plugin class for OP Permissions."""

    # Plugin metadata
    api_version = "0.11"
    name = "op_permissions"
    version = "1.0.0"
    description = "Provides permissions for structure blocks and command blocks without requiring OP status"
    
    # Define commands
    commands = {
        "opreload": {
            "description": "Reload the OP Permissions configuration",
            "usages": ["/opreload"],
            "permissions": ["op.permissions.reload"]
        }
    }
    
    # Define permissions
    permissions = {
        "op.permissions.structure_block": {
            "description": "Allows players to interact with structure blocks",
            "default": "op"
        },
        "op.permissions.command_block": {
            "description": "Allows players to interact with command blocks",
            "default": "op"
        },
        "op.permissions.reload": {
            "description": "Allows reloading the plugin configuration",
            "default": "op"
        }
    }

    def __init__(self):
        super().__init__()
        self.plugin_config: Dict[str, Any] = {}
        self.config_path: Path = None
        self.temp_ops: Set[str] = set()  # Track players with temporary OP

    def on_load(self) -> None:
        """Called when the plugin is loaded."""
        self.logger.info("OP Permissions plugin loaded!")

    def on_enable(self) -> None:
        """Called when the plugin is enabled."""
        # Set up config path
        self.config_path = self.data_folder / "config.json"

        # Load or create config
        self.load_config()

        # Register event listeners
        self.register_events(self)

        self.logger.info("OP Permissions plugin enabled!")

    def on_disable(self) -> None:
        """Called when the plugin is disabled."""
        self.logger.info("OP Permissions plugin disabled!")

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        """Grant OP to players with permissions when they join."""
        player = event.player

        # Check if player has either permission
        has_structure_perm = player.has_permission("op.permissions.structure_block")
        has_command_perm = player.has_permission("op.permissions.command_block")

        if has_structure_perm or has_command_perm:
            if not player.is_op:
                self.server.dispatch_command(self.server.command_sender, f"op {player.name}")
                self.temp_ops.add(player.name)

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        """Remove OP from players when they quit."""
        player = event.player

        # If this player had temporary OP, remove it
        if player.name in self.temp_ops:
            self.server.dispatch_command(self.server.command_sender, f"deop {player.name}")
            self.temp_ops.discard(player.name)

    def load_config(self) -> None:
        """Load the configuration file or create default if it doesn't exist."""
        # Create data folder if it doesn't exist
        self.data_folder.mkdir(parents=True, exist_ok=True)
        
        # Default configuration
        default_config = {
            "enable_structure_block_permission": True,
            "enable_command_block_permission": True,
            "debug_mode": False
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self.plugin_config = json.load(f)
                self.logger.info("Configuration loaded successfully")

                # Merge with defaults to ensure all keys exist
                for key, value in default_config.items():
                    if key not in self.plugin_config:
                        self.plugin_config[key] = value

            except json.JSONDecodeError as e:
                self.logger.error(f"Error loading config: {e}")
                self.logger.warning("Using default configuration")
                self.plugin_config = default_config
        else:
            self.logger.info("No configuration file found, creating default")
            self.plugin_config = default_config
            self.save_config()

    def save_config(self) -> None:
        """Save the current configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.plugin_config, f, indent=4)
            self.logger.info("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")

    def reload_config(self) -> bool:
        """Reload the configuration from file."""
        try:
            self.load_config()
            self.logger.info("Configuration reloaded successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error reloading config: {e}")
            return False

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        """Handle commands."""
        if command.name == "opreload":
            if self.reload_config():
                sender.send_message("§aConfiguration reloaded successfully!")
                sender.send_message(f"§7Structure Block Permission: {'§aEnabled' if self.plugin_config.get('enable_structure_block_permission', True) else '§cDisabled'}")
                sender.send_message(f"§7Command Block Permission: {'§aEnabled' if self.plugin_config.get('enable_command_block_permission', True) else '§cDisabled'}")
            else:
                sender.send_message("§cFailed to reload configuration! Check console for errors.")
            return True

        return False

