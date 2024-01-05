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

12/8
- plots
    * ~~tackler o vs dir~~
    * ~~tackler x vs y (heat map of field)~~
Clean up current plots
- ~~Remove examples that won't make contact~~
- Create one version that down samples tackles and removes Nones
Investigation
- ~~speed vs weight~~
- mometum x vs momentum y
    - ~~tackler~~
    - ~~ball carrier~~
    - ~~both on same plot~~
- ~~tackler momentum on ball carrier plane~~

12/15
- plots
    * ~~absolute value of momentum_y for all "in the plane" momentum plots~~
    * ~~match aspect ratio in momentum_x plot (first plot with lowess curves)~~
    * ~~distribution of distance~~
        - ~~for running plays almost all distances should be ~1 yard~~
- ~~data checks~~
    * ~~math on the plane of the ball carrier~~
        - ~~why is most of the data in the positive x direction? doesn't this indicate the tackler is moving in the same direction as the ball carrier? ~~
            * ~~this is what it indicates, but plotting the histogram of the direction of the tackler shows that most defenders have a direction between 0 and 180 degrees (aka are moving in the direction of the scoring end zone)~~
- ~~deep thinking~~
    * ~~interpret the momentum_x plot (first plot with lowess curves) to understand what the inflection point in the lowess curve indicates~~
        - ~~is it more likely for players to miss tackles when they are moving in the opposite direction that the ball carrier is moving?~~
        - see notebook for drawing and thinking
- ~~weight interpretation~~
    * ~~do the plots indicating speed and weight have an impact on tackles just mean that some positions are less likely to miss tackles?~~
        - ~~line backers' primary role is to make tackles so they are better at making tackles?~~
    * ~~join the position of the defenders into the dataframes~~
        - ~~plot weight v tackles separated by position~~
        - ~~summarize if position is a confounding variable~~
            * there is still some difference visible with the linebackers
- ~~pass plays~~
    * ~~repeat all of plotting with pass plays~~
    * ~~plot distances~~
        - ~~expect to see some plays where the distance is ~1 yard and some plays where the distance is smaller~~
            * ~~smaller distances would indicate the defender is less than 1 yard from the ball carrier when they catch the ball~~
    * repeat plotting but split data into two groups
        - > 1 yard at catch (frameId > 7)
        - < 1 yard at catch (frameId = 7)
    
    
12/22
interesting plots to consider
- hist/violin/box
    * speed
    * orientation and direction
    * momentum (x and y)
        - momentum x is visibly different when comparing running and passing plays (at 2 yards)
    * momentum y ball carrier
        - why is the None type so much more narrowly distributed?
    * contact angle momentum
        - check math again, is this defender momentum?
        - tackles have higher momentum in direction of ball carrier? 
            * trailing tackles?
    * contact angle
        - normalize by adding 360 to all negative contact angles?
    * contact angle momentum y
    * momentum y sum
    * y contact
        - fewer tackles are missed in the middle of the field for pass plays, doesn't apply to run plays (2 yards)
- scatter
    * speed
    * dir
    * momentum
    * momentum y (more correlated than other plots)
- other
    * orientation vs direction
        - run compared to pass
    * momentum x ball carrier vs momentum y abs ball carrier
        - run
            * remove ball carriers with negative momentum x and split plots to have ball carrier with positive momentum y on one plot and ball carrier with negative momentum y on second plot (still plot momentum y abs for both)
                - really think through what it means to need to split this data out. Is there something inherently incorrect about plotting all the data on one plot? Why are most of the defenders moving in the same x direction as the ball carrier? Does this stay consistent in the ball carrier plane plots? Why???? Plot ~20 plays with defender moving in same x direction as ball carrier? (Did the plane get rotated 90 degrees so x direction is really y direction?)
        - run compared to pass
    * momentum x vs momentum x ball carrier lowess
    * weight of linebackers 
        - 250lb bin looks like it makes more tackles and misses less tackles
            * pull out data where defender is between 240 and 250 lbs and look for an explanation
sanity checks
- runs
    * ~~restrict range to 0.8 - 1.2 yards to avoid very small distance outliers~~
- both
    * ~~check <2 yards plots~~
    * ~~visualize rotated plays~~
        - ~~consider impact on y direction metrics~~
- pass
    * ~~visualize a few plays with small distances~~
        - if splitting pass plays for defenders within small distance at time of catch, change code to include frame 6 (pass caught frame) and split dataframe where 'frame == 6' and 'frame != 6'
    * ~~confirm plays are restricted to frames after catch~~

What is the story?
momentum in different planes?
* plane of the field
    - x direction
        * why so many defenders are moving in same x direction as ball carrier
        * separate analysis for momentum_x vs momentum_x_ball_carrier
            - plot x momentum when tackler moving in same direction as ball carrier
            - plot x momentum when tackler moving in opposite direction as ball carrier
            - what to do when momentum_x_ball_carrier is negative?
                * plot separately?
                * remove?
                * normalize both ball carrier and defender values?
        * compare momentum_x between run and pass plays
    - y direction
        * momentum y violin plots
            - missed tackles have a much flatter distribution
                * more tackles are missed (proportionally) when the tackler has lots of momentum in the y direction
                    - can you say more tackles are missed when **MOST** of the tacklers momentum is moving in the y directions?
                * same applies to momentum_y_ball_carrier, but the plots look very different (dip at 0 momentum in defenders but not ball carriers) - what does this mean?
                * what is causing the large y momentum (high momentum or sharp angles)?
                * absolute momentum y - more definition in tails, help tell story
        * momentum_y vs momentum_y_ball_carrier is highly correlated 
            - use this to lead into contact angle stats (plane of the ball carrier)
* plane of the ball carrier
    - contact_angle_momentum_y_abs
        * proportionally more tackles are missed at higher momentums perpendicular to the direction of the ball carrier
    - plot contact_angle_momentum vs contact_angle_momentum_y_abs?


12/31
* Logistic Regression
    - ~~standardize~~
    - ~~confusion matrix~~
    - ~~metrics~~
    - is this useful?
* Matching
    - match on tacking data
        * momentum differences
        * plane momentum differences
    - match on ball carrier momentum data
        * plane of field differences
        * plane of ball carrier differences
* ~~Writing~~
    - ~~intro~~
    - ~~data~~
    - ~~plane of ball carrier~~
    - ~~improve current paragraphs~~
* Improvements
    - plane of ball carrier gif (rotation)
    - ~~plane comparison plot~~
        * ~~legend getting cut off, move to center~~
        * ~~add a reference at 0 degrees (either a 0 or an image)~~
    - give all plot white background (avoid text not being visible on a dark screen setting)
    - new plots
        * ~~single player~~
        * ~~position~~
        * team
* Other possible investigations
    - ~~remove all assists instead of treating assists as tackles~~
        * ~~even less distinguishing characteristics between missed tackles and tackles when no assists are included~~
    - plane comparison plot for a ball carrier (McAffery?)
    - heat map for a ball carrier

1/4
* ~~Explain why excluding forced fumbles~~
* Sideline plot
    - ~~statistical language: marginal distribution shows heavier tails in the missed tackles distributions, indicating that missed tackles happen at the extremes~~
    - **y-axis label is missing**
* ~~MORE CONCLUSION~~
    - ~~all types of momentum matter (raw, plane of the field, plane of the ball carrier)~~
    - ~~why do we care about the plane of the ball carrier~~
        * ~~it allows for interpretation of the directional momentum of the defender without needing to visualize both the ball carrier and the defender~~
        * ~~explain Preston Smith's plot~~
* Helmet Icons - left plot helmets need to shift right
* after finishing a solid submission
    - investigate logistic regression
    - investigate propensity matching
    - clean up code
    - document code


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

