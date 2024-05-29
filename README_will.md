# How To Use Google Places API for Scraping New Views with get_new_reviews.py 

1. Set up Google Places API Key:
    - You can set up a google places API key for free- this just requires you to create an account. There is a free $200 monthly credit. 

2. Declare and Assign an Environment Variable Called "GOOGLE_PLACES_KEY"
    - Once you have an API key, you need to save it to an environment variable called GOOGLE_PLACES_KEY
     - For Linux users, this is done by 
        (i) Navigating to your home directory (i.e. in the terminal, run "cd ~")
        (ii) Opening the .bashrc file (if you do not see the .bashrc file, try running "ls -a" to check for it)
        (iii) Adding the line to .bashrc: "export GOOGLE_PLACES_KEY=<\YOUR_API_KEY>" 

    - We want this environment variable to be available every time we launch a shell / terminal, so 
    we need to save this in our user configuration of our shell which is run every time the terminal is opened. In Linux 
    this is called a .bashrc file, and it can be found in your home directory (run "cd ~" and then "ls -a" to find it).
    I'm not sure how to do this on MacOS, but it is very similar for windows. 

3. Install the jsonlines package! 