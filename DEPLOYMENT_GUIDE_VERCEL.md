# How to Deploy 'StudyFlow AI' to Vercel

This guide will walk you through deploying your React (Frontend) + Flask (Backend) application to Vercel for free.

## Prerequisites
1.  **GitHub Account**: You need a GitHub account to host your code.
2.  **Vercel Account**: Sign up at [vercel.com](https://vercel.com) using your GitHub account.

---

## Step 1: Push Your Code to GitHub

First, we need to upload your code to a GitHub repository.

1.  **Open a Terminal** (Command Prompt or PowerShell) in your project folder.
2.  Run the following commands one by one:

    ```bash
    # Initialize Git
    git init
    
    # Add all files to staging
    git add .
    
    # Commit your changes
    git commit -m "Initial commit for Vercel deployment"
    ```

3.  **Create a New Repository on GitHub**:
    *   Go to [github.com/new](https://github.com/new).
    *   Repository Name: `aiml-student-assistant` (or any name you like).
    *   Make sure it is **Public** (or Private if you prefer).
    *   Click **Create repository**.

4.  **Connect and Push**:
    *   Copy the commands under *"…or push an existing repository from the command line"*. They will look like this:
    
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/aiml-student-assistant.git
    git branch -M main
    git push -u origin main
    ```
    *   Run these commands in your terminal.

---

## Step 2: Deploy on Vercel

Now that your code is on GitHub, let's deploy it.

1.  **Go to your Vercel Dashboard**: [https://vercel.com/dashboard](https://vercel.com/dashboard).
2.  Click the **"Add New..."** button and select **"Project"**.
3.  **Import Git Repository**:
    *   You should see your `aiml-student-assistant` repo in the list.
    *   Click **Import**.
4.  **Configure Project**:
    *   **Framework Preset**: Vercel should automatically detect **Vite**. If not, select "Vite".
    *   **Root Directory**: Leave it as `./` (default).
    *   **Build & Output Settings**:
        *   Build Command: `npm run build` (default is correct).
        *   Output Directory: `dist` (default is correct).
    *   **Environment Variables**: You don't have any sensitive API keys right now, so you can skip this.
5.  Click **Deploy**.

---

## Step 3: Verify Deployment

1.  Wait for Vercel to build your project (it takes about 1-2 minutes).
2.  Once finished, you will see a **"Congratulations!"** screen.
3.  Click on the **Preview** image or the **Visit** button.
4.  **Test the App**:
    *   Try uploading a syllabus file.
    *   If it generates a study plan, **Congratulations!** Your Full Stack AI App is live!

---

## Troubleshooting

*   **"Internal Server Error" on API calls**:
    *   Check the **Logs** tab in your Vercel dashboard.
    *   Function logs will show python errors.
*   **Issues with spaCy**:
    *   The deployment process should automatically install dependencies from `backend/requirements.txt`.
    *   We added code to automatically download the model (`en_core_web_sm`) if it's missing, but if it fails, check the logs.
