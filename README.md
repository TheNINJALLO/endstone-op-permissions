# OP Permissions Plugin

An Endstone plugin that provides granular permissions for Structure Blocks and Command Blocks without requiring operator status.

## Features

- **Structure Block Permission**: Grant players access to structure blocks without making them operators
- **Command Block Permission**: Grant players access to command blocks without making them operators
- **Configurable**: Enable/disable features through a config file
- **Live Reload**: Reload configuration without restarting the server
- **Operator Override**: Operators always have access regardless of permissions

## Permissions

- `op.permissions.structure_block` - Allows players to interact with structure blocks
- `op.permissions.command_block` - Allows players to interact with command blocks

## Commands

- `/opreload` - Reloads the plugin configuration (requires `op.permissions.reload` permission)

## Configuration

The plugin creates a `config.json` file in the plugin's data folder with the following options:

```json
{
    "enable_structure_block_permission": true,
    "enable_command_block_permission": true,
    "debug_mode": false
}
```

- `enable_structure_block_permission`: Enable/disable structure block permission checking
- `enable_command_block_permission`: Enable/disable command block permission checking
- `debug_mode`: Enable debug logging for troubleshooting

## Installation

1. Ensure you have Endstone server installed
2. Copy the plugin directory to your server's plugins folder
3. Start the server to generate the default configuration
4. Edit the configuration as needed
5. Use `/opreload` or restart the server to apply changes

## Usage

### Granting Permissions

To grant a player permission to use structure blocks:
```
/permission add <player> op.permissions.structure_block
```

To grant a player permission to use command blocks:
```
/permission add <player> op.permissions.command_block
```

### Revoking Permissions

```
/permission remove <player> op.permissions.structure_block
/permission remove <player> op.permissions.command_block
```

## How It Works

1. The plugin listens for `PlayerInteractEvent` when players right-click blocks
2. When a player interacts with a structure block or command block:
   - If the player is an operator, allow interaction (bypass)
   - If the player has the appropriate permission, allow interaction
   - If neither condition is met, cancel the interaction and notify the player
3. This allows fine-grained control over who can use these powerful blocks

## API Version

This plugin targets Endstone API version 0.5

## License

MIT License

## Support

For issues or feature requests, please contact the server administrators.