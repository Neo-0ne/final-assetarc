# WordPress Theme Deployment Guide

This guide provides step-by-step instructions for deploying the `assetarc-theme` to your live WordPress server.

---

There are two common methods to install a WordPress theme. The recommended method is to use the WordPress Admin Dashboard.

## Method 1: Uploading via WordPress Admin (Recommended)

This is the simplest and safest way to install the theme.

### Step 1: Create a Zip Archive of the Theme

Before you can upload the theme, you need to compress the `assetarc-theme` directory into a `.zip` file.

1.  Navigate to the root of this repository on your local machine.
2.  Find the `assetarc-theme/` directory.
3.  Compress the **entire `assetarc-theme/` directory** into a single `.zip` file. You can do this by right-clicking the folder and choosing "Compress" or "Send to > Compressed (zipped) folder". Name the file `assetarc-theme.zip`.

    **Important:** The `.zip` file should contain the `assetarc-theme` folder at its root, not just the files inside it.

### Step 2: Upload and Activate in WordPress

1.  **Log in** to your WordPress Admin Dashboard.
2.  Navigate to **Appearance > Themes** from the left-hand menu.
3.  Click the **"Add New"** button at the top of the page.
4.  Click the **"Upload Theme"** button that appears.
5.  Click **"Choose File"** and select the `assetarc-theme.zip` file you created in the previous step.
6.  Click **"Install Now"**.
7.  After the installation is complete, WordPress will show you a success message. Click the **"Activate"** link to make the theme live.

Your AssetArc theme is now installed and active.

---

## Method 2: Manual Upload via FTP/SFTP

This method is useful if your server has file upload size restrictions that prevent you from using the WordPress uploader.

### Step 1: Connect to Your Server

Use an FTP or SFTP client (like FileZilla or Cyberduck) to connect to your web server using the credentials provided by your hosting provider.

### Step 2: Navigate to the Themes Directory

Once connected, navigate to the WordPress themes directory. The path is typically:

`/path/to/your/wordpress/wp-content/themes/`

### Step 3: Upload the Theme Folder

Upload the **entire unzipped `assetarc-theme/` directory** from your local machine into the `themes/` directory on your server.

### Step 4: Activate the Theme

1.  **Log in** to your WordPress Admin Dashboard.
2.  Navigate to **Appearance > Themes**.
3.  You should now see "AssetArc Theme" listed among the available themes.
4.  Hover over it and click the **"Activate"** button.

Your AssetArc theme is now installed and active.
