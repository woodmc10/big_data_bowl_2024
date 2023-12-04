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
    * ~~watch videos of missed tackles on YouTube, then try to find in data~~
- Find a method to simplify problem
    * need a way to get to 1 frame per play that can be labeled as missed tackle
    * options
        - frame when defender is within a certain distance (3 yards? 1 yard? etc?)
            * ~~find the minimum distance between ball carrier and player who misses tackle for each play~~
                - ~~plot the distribution~~
- Weekend Reading List
    * Kaggle discussion board (starter resources and references)
    * Mentors links shared on call

11/10
- ~~Investigate tackler minimum distance~~
- practice PCA
- practice XGBoost

11/17
- Theorize Components of Tackle
    * Important parts of a tackle:
        - Reaching the same place - can’t make a tackle from looking at a ball carrier, must make contact
            * speed, direction, angle, persuit
            * how far away is the tackler from the ball carrier? (distance)
            * if both ball carrier and tackler maintain their direction and speed where will their paths cross? (distance to contact point)
            * speed and direction changes
                - juking, cutting, throwing on the breaks as techniques for avoiding tackles
                - defenders reaction time, ability to adjust to changes
        - Force at contact
            * when the tackler and the defender meet the force applied through the two players will be impacted by each one's speed, direction, size, etc
                - height and weight differential
                - angle and speed differential
                    * same speed, same angle/direction will impart much less force than same speed opposite angle/direction
                    * defenders will not have much luck making good tackles if they are stationary at the point of contact
        - Form (rugby, all of these are from a mostly head on collision type attack angle)
            * get low 
                - contact through the hips of the ball carrier
                - cheek to cheek (face to butt)
                - pick a side (don't put your head in the middle of the ball carrier's body)
                - chop your feet just before contact (the decrease in speed of your lower body and momentum of your upper body helps drop the height of your head and shoulders to improve contact position without losing all your momentum)
            * wrap arms around the ball carrier
                - front arm around mid section prevents the ball carrier from off loading to a support player
                - back arm wraps around back of leg, picking up that leg and driving prevents the ball carrier from continuing to drive their legs and make forward progress
            * drive through the ball carrier
                - make contact with the ball carrier as if you want to drive them backward into someone 1 yard behind them
        - Access
            * difficult to tackle the ball carrier if there is a blocker between the defender and the ball carrier
        - 

11/24
- Single Frame Metrics
    - make contact metrics
        - ~~tackler distance to ball carrier~~
        - ~~tackler distance to contact point~~
            - using the direction of each player, find the point where they will meet, calculate the distance between the tackler and that point
        - ~~tackler time to contact~~
            - see above calculation
            - use tackler speed to determine time to cover the distance
        - ~~ball carrier time to contact~~
            - see above, but ball carrier
        - ~~difference in time to contact~~
            - find the difference between tackler time to contact and ball carrier time to contact
        - will make contact yes/no
            - set a limit for the difference in time to contact point
            - example: assume reaching the same point 2 seconds appart will result in the tackler not making contact with the ball carrier
                - need to determine how to set the max time difference
    - force metrics
        - ~~tackler force~~
            - total (mass * acceleration)
            - north-south (trigonometry with force and direction)
            - east_west 
            - in direction of contact point (this is the same as the total because the contact point is defined to be in the direction the ball carrier and tackle are traveling)
        - ~~ball carrier force~~
            - total, north-south, east-west
        - ~~force difference~~
            - total, north-south, east-west
            - **adjust total based on angle of contact**
                - reduce the force metric based on the angle of tackler and ball carrier contact
                    - possible calculation: determine the force of the tackler in the direction the ball carrier is moving, compare that to the full force of the ball carrier
    - ~~direction and angle~~
        - difference in direction of movement and orientation
            - normalize using sine
 - other metrics that feel outside of the ability to evaluate from a single frame and may be better if aggregating over mulitple frames (will define later)
    - make contact metrics
        - ball carrier shiftiness
        - tackler adjustments
    - force metrics
        - conservation of momentum
- Code metrics
- ~~Create dataset for 1-yard distance~~
- ~~Code left/right normalization~~
                
12/1
- Check dataframe creation
    * ~~compare to number of plays in dataset~~
    * ~~spot check on play from 3 different weeks~~
- Create final dataset
    * ~~reduce to only running plays~~
    * ~~reduce to only defensive players~~
    * ~~remove all frames after tackle frame~~
    * ~~remove plays where the same player misses and makes a tackle~~
- Plot metrics
    * ~~bar plots of each numeric metric~~
    * other plots to try
        - ~~violin plots~~
        - something creative with angle plots
        - search internet for other options
        - get Lisa's ideas
    * two dimensional plots
        - ~~create 2-3 scatter plots with two dimensions~~
        - search the internet for other options
        - get Lisa's ideas
- Create outline of final notebook
- investigate rows where check_y_contact is not matching
- metrics updates
    - what to do with outliers in the make contact metrics?
    - ~~reduce the angles above 360 by subtracting 360~~
    - ~~make a scatter plot of momentum_x and momentum_x_ball_carrier~~
        * ~~try to figure out difference in momentum_x_add and momentum_x_diff~~
            - The values in the scatter plot look more quadratic than linear. Looking at the values it makes sense why the addition shows a different distribution than the subtraction.




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

