# import dependancys
from sys import exit, stdout
try:
    from praw import Reddit
    from wget import download
    from instagram_private_api import Client, ClientCompatPatch
    from PIL import Image
    from os import remove
    from time import sleep
except ModuleNotFoundError:
    print(f"missing requirements, run 'pip install -r requirements.txt'")
    exit()
# import config file
from config import config


# login to reddit and instagram
def login():
    #reddit
    reddit = Reddit(client_id=config["client_id"],
                     client_secret=config["client_secret"],
                     password=config["redditpassword"],
                     user_agent=config["user_agent"],
                     username=config["redditusername"])
    # instagram
    instagram = Client(config["instagramusername"], config["instagrampassword"])
    return reddit, instagram

# run through steps
def doit():
    submission = findpost()
    download(str(submission.url))
    size = format(submission.url)
    caption = f"{str(submission.title)}\n•\nMirrored post from r/{str(submission.subreddit)}\nCredit: u/{str(submission.author)}\nSource: https://redd.it/{str(submission)}\nBot made by: @bot_dank_memes•\n•\n•\n•\n•\n•\n•\n•\n•\n•\n•\n•\n•\n{config['hashtags']}"
    post(size, caption)

# search reddit for post
def findpost():
    print(f"Searching top posts in r/{str(config['subreddit'])}")
    submissions = reddit.subreddit(config["subreddit"]).top(time_filter="day")
    submits = 0
    for submission in submissions:
        if submission not in posted:
            print(f"Found post {str(submission.title)}, by u/{str(submission.author)}, id: {str(submission.subreddit)}")
            posted.append(submission)
            # add to previously posted so it dosent repost
            with open("files/posted.txt", "a") as f:
                f.write(f"{submission}\n")
            return submission
        else:
            submits +=1
            stdout.write(f"Submission {str(submits)} has already been posted")
            stdout.flush()
            stdout.write('\r')

# format so instagram accepts it
def format(url):
    print("\nPutting image into instagram format")
    filename = url.split("/")[-1]
    im = Image.open(filename)
    if im.width<im.height:
        bigside = im.height
    else:
        bigside = im.width
    colour = backOrWhite(im)
    background = Image.new('RGB', (bigside, bigside), colour)
    offset = (int(round(((bigside - im.width) / 2), 0)), int(round(((bigside - im.height) / 2),0)))
    background.paste(im, offset)
    if bigside > 1000:
        background.resize((1000,1000))
        bigside = 1000
    background.save("out.jpg")
    remove(filename)
    return (bigside, bigside)

# determine the colour of the background
def backOrWhite(image):
    bnw = image.convert('1')
    btotal = 0
    wtotal = 0
    for x in range(bnw.width):
        for y in range(bnw.height):
            if bnw.getpixel((x,y))/255 == 0:
                btotal += 1
            else:
                wtotal += 1
    if btotal < wtotal:
        colour = (255,255,255)
    else:
        colour = (0,0,0)
    return colour

# post to instagram
def post(size, caption):
    print("Posting to instagram\n")
    with open("out.jpg", "rb") as im:
        print(size)
        instagram.post_photo(im.read(), size, caption=caption, upload_id=None, to_reel=False)
    print("Deleting image from computer\n")
    remove("out.jpg")

# get file of previously posted images
def prev():
    posted = []
    with open("files/posted.txt", "r+") as f:
        for i in f.read().split('\n'):
            posted.append(i)
    return posted


if __name__ == "__main__":
    reddit, instagram = login()
    print(f"Logged in as {reddit.user.me()}")
    posted = prev()
    running = True
    while running:
        doit()
        print(f"Waiting {str(config['hoursBetweenPosting']*60)} minutes before posting again")
        sleep(config["hoursBetweenPosting"]*3600)
