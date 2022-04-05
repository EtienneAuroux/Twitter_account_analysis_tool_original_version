# Twitter Account Analysis Tool
### A web app to analyze twitter accounts using dash and snscrape.

Hello world,

I discovered  Dash thanks to a colleague at work and I thought it would be fun to use it for something else than ploting the data coming out of a Keithley.
So I made this app, it was a fun project and I learnt a lot!
The app runs fine locally but I fell short of being able to deploy it online (more below).
If you want to give it a try, don't hesitate to contact me :)

**You will have to install the following:**
- Python, at least version 3.7
- numpy 1.19.2
- dash 2.2.0
- dash-bootstrap-components 1.0.3
- dash-core-components 2.0.0
- dash-html-components 2.0.0
- Flask 1.1.2
- plotly 5.6.0
- snscrape 0.3.3

Note that these versions were what I had when I made the app, it will _probably_ still work if you have later versions.
I would recommend to simply start with pip install. If you encounter any module related problem try to downgrade your modules to the indicated versions.

Keep every file and subfolder in the same folder (basically just download this repo as is) and it should work just fine in your local browser on port 8050.

**Why didn't I deploy this app using Heroku or a similar PaaS?**
- Due to AWS policies, connection to snscrape servers are banned with Heroku.
- I tried to find a workaround but had to resign myself that this was not going to work :/
- I have also tried on PythonAnywhere but had the same problem.
- If you have a solution to this problem I'd greatly appreciate your help :)

**Next best thing? Make an .exe with pyinstaller! Or so I thought...** 
- I first ran into all the common problems with pyinstaller such as datapaths and "only work form cmd but not on double-click".
- Afterwards, I still had to contend with the snscrape module not being recognized.
- Ultimately, I found a workaround:
      - I pip installed snscrape into a folder in the app folder
      - Then imported directly snscrape using SourceFileLoader.load_module() function in my support_function.py file
      - The app.exe worked fine after that
- Obviously that's not a very good "shareable" solution since the app folder is now 600+ files instead of the 15-ish files I started with.

**Last comments**
So that's where I am now, the app works perfectly fine locally but sharing it for free with others (that might not know how to code) is giving me headaches.
If you read this and have a solution, please contact me!

/Etienne
