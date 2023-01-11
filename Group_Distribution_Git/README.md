# Optimized Equal Group Distribution Program

Suppose we have a group of people we want to divide into $n$ groups, with each person having unique preferences as to whom they want to be with or not. This program aims to create the most equally distributed groups based on those preferences, with the objective of making the most people as satisfied as possible. The program achieves this by categorizing and prioritizing preferences, optimizing person selection and normalizing average satisfaction through distributive justice, and optimal selection out of numerous group results (~50,000) based on quantitative measurements.

## Periods of Development  
- February 17, 2022 -  April 28, 2022

## Development Environment  
- Python 3.10  

## Motivation
The need for this program arose from an annual in-school tradition called "Outdoor Education" where each year, students from each grade spend around a week outdoors for physical health, environmental awareness, and worldview development. However, creating Outdoor Education groups had always been hugely stressful for teachers, as it was guaranteed there would be an onslaught of complaints from parents of students unhappy with their group members, causing conflict between parents and teachers, and amongst teachers themselves. 

As the G12 Student Council Vice President, I offered to create a group distribution program that systematically creates groups to satisfy the most people, in support of both teachers and students. The teachers immediately agreed, but with the request for the program to allow the user (in this case, the teachers) to have some manual control over the program. I offered for the program to be able to normalize the students' satisfaction — that is, the program would be able to decrease average satisfaction for the sake of fairer groups — to which the teachers agreed.

## Program Structure
The program requires initial data of the following:
- List of names & respective genders
- Preferences for each person

In addition, the program requires initialization of the following parameters:
- Number of groups
- Gender ratio (how evenly distributed the user wants gender to be)
- Number of iterations
- Number of expected preferences per person

As the program would most likely be run multiple times for the same group, the list of names and respective genders and the parameters will be inputted into variables at the start of the code. The user will separately input the preferences after running the program when prompted by the program UI. 

The UI is designed through Tkinter, a standard GUI library in Python.

## Terminology

### Exceptions
"Exceptions": Exceptions refer to the preferences for each person. Specifically, an exception between people $A$ and $B$ refer to whether either of $A$ or $B$ wants to be with the other, referred to as positive and negative exceptions. 
  
Positive exceptions are further categorized into tiers, as follows. The higher the tier, the higher it is weighted in the program.  
1. Tier 0 ( $A \rightarrow B$ ) :&nbsp; $A$ writes $B$ but $B$ does not write $A$.
2. Tier 1 ( $A \leftrightarrow B$ ) :&nbsp; $A$ and $B$ write each other.
3. Tier 2 ( $A \Leftrightarrow B$ ) :&nbsp; $A$ and $B$ must be put together regardless of initial preferences (referred to as Absolute Positive Exceptions)
  
Tier 0 exceptions are unidirectional, whereas Tier 1/2 exceptions are bidirectional, and are stored in the program as such.  

Negative exceptions are automatically considered absolute. The program will attempt to satisfy as many absolute exceptions as possible, even at the cost of ignoring non-absolute exceptions.

### Happiness
"Happiness": Happiness for a person $A$ refers to the number of exceptions that $A$ got fulfilled in their group. For each group distribution, this number would be unique for each person $A$, ranging from 0 to whatever number of exceptions $A$ had that was inputted into the program.

### Zero_num
“Zero_num” for each group result refers to the number of people that have none of their exceptions fulfilled. 

## Core Features  

### Greedy Algorithm
At its core, the program is a greedy algorithm that iterates through the list of people and places them in an optimal group to maximize the happiness of the current person and previous people already assigned to groups. However, this process is ultimately advantageous to those who get selected first. Therefore, a fairness function is used while iterating through the people list based on the distributive justice principle, where people with lower positive exception counts have lower opportunities to increase their happiness, and thus are chosen first for equity, whereas people with high positive exception counts are more likely to still be happy even if chosen later, and thus are less prioritized. If multiple such candidates with identical exception counts exist (which is likely), the function randomly chooses one of them for variability.

### Categorization & Prioritization of Exceptions

As explained [above](#exceptions), the inputted exceptions are categorized into tiers. Before running the greedy algorithm, the program first satisfies Tier 2 exceptions, where people with absolute negative exceptions are distributed amongst groups accordingly, with relevant people with absolute postiive exceptions being placed immediately after. The remaining Tier 0/1 exceptions are run through the greedy algorithm. This would naturally prioritize Tier 1 exceptions as they are bidirectional and thus accessed by two people, and therefore have twice the likelihood of being considered and satisfied over Tier 0 exceptions. 

### Happiness Comparison

For each iteration of the greedy algorithm, the optimal group is chosen primarily by the group that maximizes the selected person's happiness. If multiple such groups exist, then the group that maximizes the happiness of those currently in a group is chosen.  

The program runs through and saves ~50,000 group results (specific number is inputted by user before running program). At the end, the final group, chosen by the lowest zero_num and highest average happiness (in that order), is displayed. 

### Normalization of Happiness via Distributive Justice - Transferring Exceptions

The program prioritizes low zero_num and high average happiness, with such factors chosen to increase the number of people satisfied with their groups. However, prioritizing those factors to produce ideal groupings might actually have contradictory results.  

For example, a result like the following:

| % of Exceptions Satisfied | 0% ~ 20% | 20% ~ 40% | 40% ~ 60% | 60% ~ 80% | 80% ~ 100% |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **% of People** | 5% | 5% | 20% | 30% | 40% | 

might fit the criteria, but the user (and the people) may feel as if the large majority of people received ideal groupings at the sacrifice of a select few, with the disparity between the happy and unhappy being too apparent.  

In lieu of fairness and equality, the user might prefer a result like the following: 

| % of Exceptions Satisfied | 0% ~ 20% | 20% ~ 40% | 40% ~ 60% | 60% ~ 80% | 80% ~ 100% |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **% of People** | 5% | 10% | 25% | 30% | 30% | 

where although the average happiness may be lower and the groupings less ideal, more people would be satisfied and less people angry with the results. In other words, to achieve maximum satisfaction, the most ideal groupings may actually not be preferable.  

The program offers an option to the user to make their groupings "less ideal" for fairness, for use at their discretion. 

It achieves this through a "Transfer Exceptions" button that transfers Tier 1 positive exceptions to Tier 0. Specifically, it chooses a person $A$ with the highest number of Tier 0/1 positive exceptions, and a person $B$ among $A$'s Tier 1 exception recipients with the highest number of Tier 0/1 positive exceptions. It then removes the exception from $A$ to $B$, turning $A \leftrightarrow B$ into $A \leftarrow B$. (We could also randomly remove one of $A$'s Tier 0 exceptions, but removing Tier 1 exceptions affects both $A$ and $B$, and thus is more effective.) The program repeats this process $n$ times ( $n$ specified by the user upon request), after which it re-runs the group distribution algorithm to display new "fairer" group results.

<details>
  <summary>(Further Explanation)</summary>
  
  ### Transferring Exceptions - Further Explanation
  Let us explore why this works. A person's happiness is solely determined by how many of their exceptions are satisfied. Thus, every exception can be considered as an opportunity for the person(s) in question to become happy. 
  
  If a Tier 0 exception $A \rightarrow B$ is satisfied, $A$'s happiness increases, but $B$'s happiness does not.  
  If a Tier 1 exception $A \leftrightarrow B$ is satisfied, both $A$ and $B$'s happiness increases. 
  This also applies to Tier 2, but Tier 2's exceptions are handled separately, and thus are not considered when transferring exceptions.

  Thus, the person with the most Tier 0 and 1 exceptions has the most chances to become happy, even if the program selects that person later at a disadvantage via the [fairness function](#greedy-algorithm). Our aim is to decrease such person's chances by removing exceptions, as overall this would allow more opportunities for people with less Tier 0/1 exceptions to become happy. 

  Let there be a Tier 1 exception $E_1$ with person $A$ and $B$ ( $A \leftrightarrow B$ ), where $A$ is the person with the most Tier 0/1 exceptions. When the program runs, both $A$ and $B$ have two chances to be happy via $E_1$, as $E_1$ has a chance to be considered when the program selects $A$ and $B$.  

  Now let us transfer $E_1$ to a Tier 0 exception $E_0$ by removing $A \rightarrow B$ ( $E_0 = B \rightarrow A$ ). $A$ can now no longer become happy via $E_0$; thus, $A$'s chances to increase happiness is decreased by 2.  

  However, this also decreases $B$'s chances of becoming happy by 1. Thus, $B$ is chosen to be the person with the most Tier 0/1 exceptions among $A$'s Tier 1 recipients. This effectively decreases both $A$ and $B$'s chances with one transfer. 
</details>

## Reference  
- John Rawls, 1971, A Theory of Justice
