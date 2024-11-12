
# Momentum and Missed Tackles
## Introduction
In contact sports like football, momentum is a critical component, and tackling is an excellent example of a sports collision. The Law of Momentum Conservation governs collisions in physics. It states that momentum in a collision cannot be created or lost but must remain the same before and after the event, such as a tackle. Although football is a complex sport in the real world and cannot be fully explained by this single law, the concept of momentum conservation provides an interesting platform to study football tackles. This investigation focuses on deriving actionable insights for both offensive and defensive strategies by analyzing the momentum of the ball carrier and the defender, with the goal of enhancing performance outcomes.

### What is Momentum?
Momentum is a concept in physics that describes the motion of an object. It is the product of an object's mass and its velocity, which includes information about the direction. In simple terms, momentum in a tackle scenario can be thought of as the "driving force" that both players have due to their mass and speed. The one with greater momentum at the time of collision is likely to have a dominant impact in the tackle.

## Data Collection Method
The available tracking data was analyzed to identify the frames of running plays where defenders were positioned approximately 2 yards away from the ball carrier. The distance of 2 yards was chosen to ensure defenders were more than an arm's distance away, meaning contact was imminent but had not occurred. A small cushion was allowed to account for the frame sampling rate, so defenders between 1.8 and 2.2 yards away from the ball carrier were included in the data set. The tackles group included assists, but forced fumbles were excluded from the analysis because there is no way to know if the defender would have completed the tackle after forcing the ball out. The dataset was further refined by projecting the point of contact between the defender and the ball carrier. If this point was located behind either player or outside the field of play, the data point was removed. Finally, the number of tackles was down-sampled to match the number in the missed tackles group.

## Raw Momentum
To investigate the impact of tackles, we can analyze the momentum of the ball carriers and defenders separately. In the imagined perfect collision the object with more momentum will continue moving. Considering the ball carrier as one of the objects in the collisions, missed tackles occur when the momentum of the ball carrier is not stopped by the defender. By using a histogram of the ball carrier momentum, we can see that missed tackles occur more frequently when the ball carrier has more momentum. In football, this aligns with intuition, as a ball carrier with more momentum is more likely to break through attempted tackles.

<fig 1 here>
Fig. 1: Ball Carrier Momentum Histogram

The histogram depicting the defender's momentum shows a consistent pattern as the ball carrier's momentum plot. Higher momentum leads to a greater likelihood of missed tackles. This trend may not be helpful when tackles are considered to be a perfect system, but it aligns with football intuition. An increase in momentum often results in a decrease in control and precision. As a result, defenders may be unable to execute a perfect hit or wrap the ball carrier to bring them down, or they could overcommit to an angle of pursuit and miss the ball carrier entirely.

<fig 2 here>
Fig. 2: Defender Momentum Histogram
**Raw Momentum Summary**
🏈 Ball Carriers: keep the momentum high, break through tackles
🏈 Defenders: control the momentum, make solid contact

## Momentum in the Plane of the Field
Momentum is an important aspect of many sports. It is a vector measurement that can be expressed in terms of magnitude and direction. To determine how much momentum is moving toward the scoring endzone versus the sidelines, the components of the momentum are calculated. Positive endzone momentum moves towards the scoring endzone and negative endzone momentum moves away from it.

### Endzone Momentum
When examining the tackling technique, plotting the endzone momentum of the ball carrier against the endzone momentum of the defender provides more detailed information. The plots are separated to distinguish defenders with momentum away from the scoring endzone from defenders with momentum towards the scoring endzone. In both plots the ball carrier's momentum is moving toward the scoring endzone.

In the plot with the defender's momentum moving away from the scoring endzone, the trendlines for both successful and missed tackles show a negative correlation. This suggests that defenders more often have higher momentums when they are moving downhill to attempt tackles against ball carriers who have not yet built up speed in their run. The trendlines are not parallel, but instead intersect at approximately 600 yards per second of defender momentum. The crossing trendlines indicate that the significance of ball carrier and defender momentum varies in their contribution to successful and missed tackles depending on which one is higher. Since it is rare for the ball carrier to have a large momentum when the defender has a large momentum moving away from the endzone, these situatations more commonly lead to missed tackles. This could be due to ball carriers making changes in direction or acceleration because they have not yet built up momentum.

When a defender's momentum is toward the scoring endzone, the slight positive correlation observed between the defender and ball carrier momentum is even more pronounced. This is reasonable because defenders who trail the ball carrier must match or exceed the speed of the ball carrier in order to catch up with them. The trendlines still demonstrate that higher ball carrier momentum results in more missed tackles, as is seen with the non-directional momentum measures.

<fig 3>
Fig. 3: Endzone Momentum Scatter Plot
### Sideline Momentum

The interesting relationship between the defender and ball carrier endzone momentum is not present in the sideline momentum. When the players' sideline momentums are plotted a strong positive correlation is present. The ball carrier momentum toward either the left or the right sideline requires the defender to drive their momentum in the same direction in order to make contact. One interesting note from this plot, marginal distributions show heavier tails in the missed tackles indicating that missed tackles happen at the extremes of sideline momentum.

<fig 4>
Fig. 4: Sideline Momentum Scatter Plot
**Plane of the Field Momentum Summary**
🏈 Ball Carriers: when your momentum is low be shifty, when your momentum is high keep going
🏈 Defenders: don't be in the extremes where missed tackles are more common, stay in control

## Momentum in the Plane of the Ball Carrier
The plane of the field is easy to picture at any moment because the orientation does not change as the play continues. This is not the case with the plane of the ball carrier because the movement of the player establishes the plane. Imagine a square on the field centered on the ball carrier. If this square remained in the plane of the field, the markings would always stay vertical and horizontal in this square as the ball carrier runs across different parts of the field. But if this square was anchored to the frame of the ball carrier, the markings would change orientation based on the direction the ball carrier movement. This could be disorienting for viewers, but it can provide valuable information about the defender's movements in relation to the ball carrier.

<GIF>

Fig 5: Plane of Ball Carrier GIF
### Momentum Perpendicular to the Ball Carrier

When adjusting the plane of momentum, it becomes easier to analyze the details of momentum directed to either side of the ball carrier. This perpendicular momentum is demonstrated in a violin plot that shows an increase in missed tackles when momentum is directed to the left of the ball carrier. It is likely that this is a side effect of the small sample size of missed tackles.

There is a difference in width and height between the distribution which indicates that fewer tackles are missed when less of the defender's momentum is directed perpendicular to the ball carrier. Defenders attacking the ball carrier with most of their momentum traveling perpendicularly, which happens when they are closer to a right angle with the ball carrier, are more likely to miss tackles. Additionally, the longer tails in the missed tackles distribution suggest that there are more missed tackles when more of the defender's momentum is directed to the left or right of the ball carrier.

<fig 6>
Fig 6: Perpendicular Momentum Violin Plot
### Momentum Parallel to the Direction of Ball Carrier Movement

When assessing the defender's momentum in the plane of the ball carrier, the direction of the ball carrier's momentum is used to find the angle of intersection and determine how much of the defender's momentum is moving in the same direction. Decomposing the momentum into the plane of the ball carrier shows that only a handful of missed tackles occur when the ball carrier's momentum is less than 500 yards/sec, no matter whether the defender's momentum is moving in an opposing direction to the ball carrier or in a consistent direction.

<fig 7>
Fig. 7: Parallel Momentum Scatter Plot
**Plane of the Ball Carrier Momentum Summary**
🏈 Ball Carrier: make the defenders take a sharp angle
🏈 Defender: if you must tackle a ball carrier at a sharp angle, remember "slow is smooth, smooth is fast," stay in control

## Player Analysis
The importance of momentum in tackle analysis is clearly visible starting with the ball carrier's raw momentum plotted in Fig 1 through the parallel momentum impacts seen in Fig 7. Whether it is the raw magnitude of momentum, momentum in relation to the field, or momentum in relation to the ball carrier, it is a impactful factor. Evaluating momentum in the plane of the ball carrier, in particular, can help visualize the direction of the defender in relation to the ball carrier without having to plot them separately.

Two plots have been provided to illustrate the directional momentum of outside linebacker Preston Smith. The left plot shows Smith's momentum in relation to the field, with the endzone direction set by the horizontal line. The blue bars represent missed tackles and are spread around all angles, while the orange bars represent successful tackles and are somewhat clustered in the lower right but generally present around all angles.

The right plot provides a clearer picture by assessing Smith's momentum in relation to the ball carrier. The horizontal line sets the direction of the ball carrier, with the ball carrier's momentum moving to the right. In this plane, it is easier to see that Smith is more likely to miss tackles when his momentum is moving in a very similar direction to that of the ball carrier. When Smith can attack from less acute angles, he is able to complete more of his tackles. With this information, a coach and Smith can investigate his position, movement, and attack angles in these plays and identify opportunities for improvement in Smith's attempted tackles.

<fig 8>
Fig. 8: Preston Smith Tackle Plane Comparison
## Future Work
This work has provided metrics that will allow coaches and players to anlayze performance and find small improvements for making and breaking tackles. In the future I would like to explore the impact on ball carriers' changes in momentum in the frames following this selected frame. My hypothesis is that ball carriers with higher momentum would benefit from continuing in the current direction and maintaining direction, while ball carriers with lower momentum would benefit from shifting and changing directions.

## Acknowledgements
Mentor: I would like to thank Zach Stuart for all of his thoughtful comments and questions through the entire project

Frame Visuals: The code to visualize frames for the plane of ball carrier explanation GIF was adapted from Morgan Martin's NFL Data Bowl 2023: Initial Pass Set Kick Speed

Author: Martha Wood

Code: Git
