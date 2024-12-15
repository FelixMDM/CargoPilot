# CargoPilot Software

## Overview

Welcome to our senior design project for CS179M (AI) at UCR! This Flask-powered web application is designed to assist dockyard crane operators by providing an intuitive and efficient tool to calculate the optimal unloading and loading and blancing paths for container ships.

## Project Setup Guide

### To run this project:

* Clone the repository.
* Open two separate terminal windows (e.g., in VSCode):
  * **In the first window:**
    * Navigate to the **client** folder: *`cd` into "client"*
    * Run the following commands:
      * `npm i` (ensure you have Node.js installed; if not, there are many tutorials available online)
      * `npm run dev` to start the project on localhost
  * **In the second window:**
    * Navigate to the **server** folder: *`cd` into "server"*
    * Set up a virtual environment:
      * Create a virtual environment named **venv** (as specified in `.gitignore`)
      * **Note for Windows users:** You may need to adjust permissions if creating the venv is blocked. Run:
        * `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
      * Commands for creating and activating the virtual environment:
        * **Windows:** `python -m venv venv` -> `venv/Scripts/activate`
        * **Linux/Unix:** `virtualenv venv` -> `source venv/bin/activate`
    * run `pip install -r requirements.txt`
    * Start the server by running *`python server.py`*
    * Now, navigate back to **localhost** in your browser to see your frontend interacting with API calls.
   
    # Prototype link:
    * https://www.figma.com/proto/GeJhQNc8f5Wv8bKPBnDRGC/WireFrame-CargoPilot?node-id=0-1&t=DZZyThVtM04yp12m-1
