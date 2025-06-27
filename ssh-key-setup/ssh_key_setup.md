# SSH Key Setup Tutorial

## Overview

SSH (Secure Shell) keys provide a secure way to authenticate with remote servers without using passwords. This tutorial will guide you through generating SSH keys and configuring them for remote server access.

## Prerequisites

- A local computer with terminal/command line access
- A remote server you want to connect to
- Basic familiarity with command line operations

## Step 1: Check for Existing SSH Keys

Before generating new keys, check if you already have SSH keys on your local machine:

```bash
ls -la ~/.ssh
```

Look for files named `id_rsa` and `id_rsa.pub` (or `id_ed25519` and `id_ed25519.pub`). If these exist, you can skip to Step 3.

## Step 2: Generate SSH Key Pair

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**Note**: Ed25519 keys are more secure and faster than RSA keys.

### Key Generation Process

1. When prompted for file location, press Enter to use the default location
2. Enter a secure passphrase when prompted (optional, you will need to enter this everytime you login though)
3. Confirm the passphrase

The command will generate two files:
- Private key: `~/.ssh/id_ed25519` (keep this secret!)
- Public key: `~/.ssh/id_ed25519.pub` (this can be shared)

## Step 3: Copy Public Key to Remote Server

### Method 1: Using ssh-copy-id (Easiest)

```bash
ssh-copy-id suppal@server_ip_address
```

Replace `username` with your remote server username and `server_ip_address` with the server's IP address or domain name, eg. `ssh-copy-id sidd@della9.princeton.edu`

### Method 2: Manual Copy

If `ssh-copy-id` isn't available, manually copy the key:

1. Display your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

2. Copy the entire output to your clipboard

3. Log into your remote server:

```bash
ssh sidd@della9.princeton.edu
```

4. Create the `.ssh` directory (if it doesn't exist):

```bash
mkdir -p ~/.ssh
```

5. Add your public key to the authorized keys file:

```bash
echo "your_public_key_here" >> ~/.ssh/authorized_keys
```

6. Set proper permissions:
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

## Step 4: Test SSH Key Authentication

Try connecting to your server using SSH keys:

```bash
ssh sidd@della.princeton.edu
```

If configured correctly, you should be able to log in without entering a password (unless you set a passphrase for your key).

## Step 5: Configure SSH Client (Optional)

Create an SSH config file to simplify connections:

```bash
nano ~/.ssh/config
```

Add an entry for your server:

```
Host princeton
    HostName della.princeton.edu
    User sidd
    IdentityFile ~/.ssh/id_ed25519
```
Now you can connect simply with:

```bash
ssh princeton
```

In case you need to setup a proxy jump or a tunnel, eg. when you need to first log on to the login node and then go to the main server. You can do the following do avoid the multiple steps.

```bash
nano ~/.ssh/config

Host cornell
    HostName cbsumoeller.biohpc.cornell.edu
    User suppal
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump sidd@cbsulogin.biohpc.cornell.edu
```

```bash
ssh cornell
```

## Multiple servers

### Multiple Keys for Different Servers (recommended)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_server1 -C "server1@example.com"
ssh-keygen -t ed25519 -f ~/.ssh/id_server2 -C "server2@example.com"
```

Add the key to `~/.ssh/authorized_keys` in the remote server.

Configure in `~/.ssh/config`:

```bash
Host server1
    HostName server1.example.com
    User username
    IdentityFile ~/.ssh/id_server1

Host server2
    HostName server2.example.com
    User username
    IdentityFile ~/.ssh/id_server2
```

### Use the same key for multiple servers

Add the old key to `~/.ssh/authorized_keys` in the remote server.

```bash
nano ~/.ssh/config

# Already present
Host cornell
    HostName cbsumoeller.biohpc.cornell.edu
    User sidd
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump sidd@cbsulogin.biohpc.cornell.edu

# New
Host cornell2
    HostName cbsumoeller02.biohpc.cornell.edu
    User sidd
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump sidd@cbsulogin.biohpc.cornell.edu
```

## Security Best Practices

### Protect Your Private Key
- Never share your private key (`id_ed25519`)
- Set appropriate file permissions: `chmod 600 ~/.ssh/id_ed25519`

### Regular Key Rotation
Consider generating new keys periodically and removing old ones from servers.

## Troubleshooting

### Permission Denied (publickey)
- Verify the public key is correctly added to `~/.ssh/authorized_keys`
- Check file permissions on the server
- Ensure you're using the correct username and server address

### Connection Refused
- Verify the server's SSH service is running
- Check if you're using the correct port (default is 22)
- Confirm firewall settings allow SSH connections

### Key Not Found
- Verify your private key path with `ssh -v username@server_ip`
- Use `-i` flag to specify key location: `ssh -i ~/.ssh/id_ed25519 username@server_ip`

## Conclusion

SSH keys provide a secure and convenient way to authenticate with remote servers. By following this tutorial, you've learned how to generate keys, configure them on servers, and implement security best practices. Remember to keep your private keys secure and consider using SSH agent for improved workflow efficiency.