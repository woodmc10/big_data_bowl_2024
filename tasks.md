10/20
- ~~download data~~
- ~~visualize single frame~~
- ~~animate single play~~
- EDA
    * ~~which player is the ball carrier~~
    * which defensive player is closest to the ball carrier
- Reading list for weekend
    * ~~Kaggle discussion board~~
        - come back to Starter resources and references
    * Mentors links shared on call (bookmarks)
    * ~~at least one neural network submission notebook~~


10/27
- ~~pick a tool for code management~~
    * ~~cookiecutter~~
- ~~pick a tool for data management~~
    * ~~dvc~~
        - ~~can't figure out how to get it installed. Giving up, probably don't need for this.~~
- ~~create git repo~~
- explore kaggle interface
- ~~EDA~~
    * ~~How many missed tackels in the dataset?~~
        - ~~How many on run plays, how many on pass plays?~~
    * Does it appear the missed tackles match with first contact events?
        - How often is there a first contact on a play that has a missed tackle?
        - How often is the first contact in a frame where the defender who missed the tackle is closest to the ball carrier?
- try to come up with a direction/path
    * **missed tackle probability?**
        - offensive forced missed tackles (PFF stat)
            * can I get access to this stat?
                - cannot find it at the play level, may be able to get a total for the year, but that doesn't feel very helpful
            * can I match it to the frame data I have?
            * can I come up with an interesting research approach 
        - reasons a defender misses the tackle?
            * talk to a football coach about the reason for missed tackles
                - determine which of these can be identified in the data
            * scorecard?
                - for college players coming to the draft?
        - research
            * watch videos of missed tackles on YouTube, then try to find in data
- Reading list for weekend
    * ~~Notebook Zach shared for determining when pressures happened~~
        - ~~think about how to code this for determining when missed tackles happen~~
            * **This is a finalist submission, the approach is impressive in its approach and complexity. It would take me the whole 3 months to try to replicate it. I need to find a simpler approach to predicting missed tackles for this winter. I'd like to revisit this after the competetion ends and try to replicate it.**
    * Kaggle discussion board (starter resources and references)
    * Mentors links shared on call
    * ~~PFF forced missed tackles stat~~ 
        - how do they determine and track this? - it is a proprietary stat determined by analysts (I think while they watch video)
    * research on missed tackles?

11/3
- EDA
    * ~~Does it appear the missed tackles match with first contact events?~~
        - ~~Are all 23 rows per frame labeled with first contact event?~~
            * yes
        - ~~How often does the first contact frame have the defender who missed the tackle closest to the ball carrier?~~
            * ~~find missed tackler distance from ball carrier in these frames~~
                - mean: 2.2 yards
            * ~~get a count of the number of missed tackle plays that don't have a first contact event~~
                - in week 1: 6 plays
- research
    * watch videos of missed tackles on YouTube, then try to find in data
- Find a method to simplify problem
    * need a way to get to 1 frame per play that can be labeled as missed tackle
    * options
        - frame when defender is within a certain distance (3 yards? 1 yard? etc?)
            * find the minimum distance between ball carrier and player who misses tackle for each play
                - plot the distribution
- Weekend Reading List
    * Kaggle discussion board (starter resources and references)
    * Mentors links shared on call

TODO: Data Adjustments
- switch all plays to run from left to right


# Convos with Zach
## 11/2
Pressure Probability Notebook:
custom loss function - compute the loss on each frame, only take the frame with the minimum loss to update gradients
this is a complex solution that would probably take me the full 3 months to understand and implement

simplify problem - one frame per play
every play, 0.5 sec before first contact -> this is leaky because it is moving the wrong way in time
first frame where a defender is 3 yards from the runner
**need to come up with the method that can be used for this**

first contact tag - does it tag every player for a single frame? Is the nearest player to the runner labeled as a missed tackle?
Zach imagines first contact will not often/always be a missed tackle

Example of a final goal (insite):
- Investigate defenders setting the edge - is there a situation/scenario/scheme/etc that results in more missed tackles?

