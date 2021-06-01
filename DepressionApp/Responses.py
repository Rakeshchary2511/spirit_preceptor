import random

songs = [
    "'Weightless', by Marconi Union",
    "'Electra', by Airstream",
    "'Mellomaniac (Chill Out Mix)', by DJ Shah",
    "'Watermark', by Enya",
    "'Strawberry Swing', by Coldplay",
    "'Please Don’t Go', by Barcelona",
    "'Pure Shores', by All Saints",
    "'Someone Like You', by Adele",
    "'Canzonetta Sull’aria', by Mozart",
    "'We Can Fly', by Rue du Soleil (Café Del Mar)",
    "'All of the Stars', - Ed Sheeran",
    "'Beautiful', - Christina Aguilera",
    "'Born This Way', - Lady Gaga",
    "'Don't Stop Believin', - Journey",
    "'FireFly', - Ed Sheeran",
    "'Fooling Yourself', - Styx",
    "'GIRL', - Maren Morris",
    "'Grand Illusion', - Styx",
    "'He Will Hold Me Fast', - Keith & Kristyn Getty",
    "'Hero', - Mariah Carey",
    "'Higher Power', - Boston",
    "'I'm Alive', - Kenny Chesney (with Dave Matthews) ",
    "'Inner Demons', Be Alright -The Ramones",
    "'I Will Always Love You', - Whitney Houston",
    "'I Won't Back Down', - Tom Petty and the Heartbreakers",
    "'Healing Meditation', - Angus Woodhead",
    "'Only Time', - Enya ",
    "'Not Dead Yet', - Styx",
    "'Seasons of Love', - Rent ",
    "'Shades Official Music Video', - by Manas Jha",
    "'Somewhere in Time', - John Barry",
    "'This is It', - Kenny Loggins",
    "'Unwell', - Matchbox Twenty",
    "'When the Seasons Change', - Five Finger Death Punch",
    "'Wonder', - Natalie Merchant",
    "'You Raise Me Up', - Josh Groban",
]


booksSupport = [
    """Stop Negative Thinking Now.
    Learn to stop negative thoughts before they start.
    Just read the Book suggested below which will help you overcome from your unconscious level,
    by showing you how to let negative thoughts drift by without taking any notice.""",
    """Beat the Everyday Blues
    Learn to let go of pervasive worry and relax into better everyday mood.
    Now have a look at the book suggested below which will help you how to form a strategy to perk up quickly
    when you start feeling down,
    and change your overall mood to a more upbeat and optimistic one.""",
    """Self Sabotage
    Stop listening to your own negative 'hype'.
    Take a look at the below mentioned book which challenges your hurtful thoughts about yourself and stop you
    from blowing one bad experience out of proportion.""",
    """Stop Complaining
    Break the complaining habit and learn to relax with imperfections and irritations.
    Go and download suggested Book which will turn off your ‘auto-complaint’ switch,
    letting you consciously choose your battles and to relax with the imperfections of life at other times.""",
    """Dealing with Disappointment
    Build in flexibility to your expectations and manage disappointment and set-back gracefully.
    Have a look at the below Book will teach you how to manage your expectations better so they’ll be much more realistic,
    meaning you won’t constantly be feeling let down.""",
    """Dealing with Guilt
    Break the pattern of feeling guilty or ashamed, and take a new view.
    Below mentioned Book will help make the process of guilt clearer to you so you can refuse to be controlled by it.""",
    """See the best in others
    Move from viewing others with cynicism and suspicion to a more realistic and sympathetic understanding.
    Go and grab the Book from any Online store which tries to develop and enhance your capacity to judge people neutrally, not negatively,
    until you get to know them.""",
    """ No Regrets
    Stop wallowing in your past and start learning from your experiences and move on.
    Get the Book as your First priority and cover all pages of that book
    which will stop you from getting so caught up in focusing on the losses and errors of your past,
    so you can concentrate on the present and the future.""",
    """Improve Your Mood
    Relax deeply and cast off black moods.
    Take a look at the below mentioned book which will enable your unconscious mind to bring forth a new,
    more relaxed, more upbeat emotion.
    You’ll also gain perspective on whatever was making you feel bad.""",
    """No Excuses
    Develop a deeper honesty and truthfulness with yourself and take full responsibility for what you do.
    This mentioned Book will help you understand your own and others
    motivations more clearly.""",
]


quotes = [
    """Don’t let life discourage you; everyone who got where he is had to begin where he was.""",
    """There is hope, even when your brain tells you there isn’t.""",
    """Give yourself another day, another chance. You will find your courage eventually.
     Don’t give up on yourself just yet.""",
    """You say you’re ‘depressed’ – all I see is resilience.
    You are allowed to feel messed up and inside out.
    It doesn’t mean you’re defective – it just means you’re human.""",
    """Those who have a ‘why’ to live, can bear with almost any ‘how’.""",
    """Even if you’re on the right track, you’ll get run over if you just sit there.""",
    """Our greatest glory is not in never falling, but in rising every time we fall.""",
    """Suffering has been stronger than all other teachings and has taught me to understand what your heart used to be.
    I have been bent and broken, but – I hope – into a better shape.""",
    """It’s not whether you win or lose, it’s how you play the game.""",
    """Self-care is never a selfish act—it is simply good stewardship of the only gift I have,
    the gift I was put on earth to offer to others.""",
    """I’ve learned that everything happens for a reason,
    every event has a why and all adversity teaches us a lesson…
    Never regret your past. Accept it as the teacher that it is.""",
    """Whether we have it all or we have nothing,
    we are all faced with the same obstacles: sadness, loss, illness, dying and death.
    If we are to strive as human beings to gain more wisdom, more kindness, and more compassion,
    we must have the intention to grow as a lotus and open each petal one by one.""",
]

books = [
    """The Antidote: Happiness for People Who Can’t Stand Positive Thinking""",
    """The CBT Toolbox: A Workbook for Clients and Clinicians""",
    """Change Your Brain, Change Your Life""",
    """Feeling Good: The New Mood Therapy""",
    """Re-Create Your Life by Morty Lefkoe""",
    """The Happiness Trap’ By Dr. Russ Harris """,
    """The Stress-Proof Brain By Melanie Greenberg""",
    """The Happiness Track By Emma Seppala""",
]

booksSupportLen = len(booksSupport)
booksLen = len(books)
songLen = len(songs)
quotesLen = len(quotes)


def motivationPost():
    suggestion = {
        "quote": random.choice(quotes),
        "bookSupport": random.choice(booksSupport),
        "book": random.choice(books),
        "song": random.choice(songs),
    }
    return suggestion
