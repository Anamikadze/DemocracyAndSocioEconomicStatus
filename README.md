# Exploring the Influence of State Dependency on Regime Preferences in Post-Communist Europe and Central Asia
## Summary
In this research project, I replicate and extend the analysis presented in the book Autocratic Middle Class (Rosenfeld, 2020),  which investigates the influence of state dependency on the demand for democracy in post-communist Europe and Eurasia. My focus is on the book's third chapter, which offers a cross-national examination of the regime preferences of the post-communist middle class. By replicating the author's study, I demonstrate that the middle class's demand for democracy is more contingent than previously believed, with increased support for democracy observed only among those employed in the private sector in non-democratic states. Furthermore, I expand the scope of analysis to include individuals exhibiting the greatest reliance on the state, such as those receiving unemployment and disability benefits, social assistance, and welfare transfers. My findings indicate that among various socio-economic groups, those receiving state assistance are the least likely to support democracy as a regime, thereby providing a deeper understanding of the relationship between state dependency and democratic preferences.
## Data
In this study, I utilize data from the European Bank for Reconstruction and Development's (EBRD) Life in Transition Survey (European Bank for Reconstruction and Development. (2006). Life in Transition Survey (LiTS). Retrieved from https://rb.gy/51rgv), conducted in early 2006. The dataset comprises nearly 27,000 individual observations across 27 countries from Central and Eastern Europe and the former Soviet Union. This unique dataset includes information on both employment history and regime preferences.

For the purpose of our analysis, I divide the data into two sub-samples: democratic countries 
(N = 18) and non-democratic countries (N = 9). The democratic countries in the sample include Albania, Bulgaria, Croatia, Czech Republic, Estonia, Georgia, Hungary, Latvia, Lithuania, Macedonia, Moldova, Montenegro, Poland, Romania, Serbia, Slovak Republic, Slovenia, and Ukraine. Non-democratic countries consist of Azerbaijan, Armenia, Belarus, Kazakhstan, Kyrgyzstan, Russia, Tajikistan, and Uzbekistan.

While the original study's author does not explicitly state the index or method used for classifying the countries, my research indicates that the classification aligns with the Economist Intelligence Unit's Democracy Index (Economist Intelligence Unit. (2006). Democracy Index. Retrieved from https://rb.gy/8t1h1). The democratic sub-sample encompasses full democracies and flawed democracies, while the non-democratic sub-sample includes hybrid and authoritarian regimes. Notably, Georgia and Ukraine were classified as hybrid regimes by the Economist Democracy Index in 2006. However, the author acknowledges that these countries were on the cusp of democracy and includes them in the democratic sub-sample; I follow the same approach in my analysis.
## Methodology and Variables
This study aims to explain regime preferences across 27 countries, focusing on the relationship between socio-economic dependency on state and support for democracy.

### Democracy

Following the original study author’s approach, I measure democracy using two components. The first component, 'democracysupport', captures the preference for democracy through a survey question that asks respondents which statement they agree with most: (1) Democracy is preferable to any other form of the political system; (2) For people like me, it does not matter whether a government is democratic or authoritarian; or (3) Under some circumstances, an authoritarian government may be preferable to a democratic one. I code 'democracysupport' as one for those who believe democracy is preferable and zero otherwise.

The second component, 'instsupport', measures respondents' beliefs regarding the importance of various democratic institutions, including: (1) free and fair elections, (2) freedom of speech, (3) an independent press, (4) courts that defend individual rights against abuse by the state, (5) equality before the law, (6) minority rights, and (7) a strong political opposition. I code 'instsupport' as one for those who strongly believe that all of the aforementioned institutions are important.

The dependent variable 'democracy' is a product of 'democracysupport' and 'instsupport'. Later, I relaxed the definition of democracy to include individuals who “somewhat agree” that the above-metntioned institutions are important.

### Middle Class 

To define the middle class, I adopt the author's approach, identifying middle-class individuals as upper- or lower-level managers, professionals, or small-business owners who have graduated from a four-year college or university. This study employs a sociological definition of the middle class (Fitzgerald, 2012), rather than an income-based definition, for several reasons.

First, during the early 2000s, official salaries in transition economies often failed to accurately reflect an individual's income due to the widespread presence of informal job markets (Lehmann & Pignatti, 2007). Second, utilizing an income-based definition in post-communist countries could be challenging because corruption was rampant, and people often obtained money from illegal sources, which they might not self-report in surveys. Lastly, social desirability bias might lead some respondents to report higher salaries than they actually earned. By using a sociological definition of the middle class, I mitigate the potential inaccuracies that might arise from relying on income-based definitions in the context of post-communist countries with extensive informal economies and corruption.

To operationalize middle class, I code 'education' as one for individuals with a university or postgraduate degree and zero otherwise. We code 'occupation' as one for individuals who fall under three categories: technicians & associate professionals, professionals, and managers, and zero otherwise. The independent variable 'middleclass' is a product of the 'education' and 'occupation' variables.

### State Employment
I code 'state employment' as one for individuals employed in the state sector and zero otherwise. Additionally, I create sub-groups of state employment, including state-employed educators, health professionals, and administrators to explore differences in regime preferences for seperate groups.

### State Assistance
I code 'state assistance' as one for individuals who received state-provided benefits, such as unemployment allowance, social assistance, and disability benefits, and zero otherwise.

### Control Variables
To account for differences in regime preferences across age groups, I include age and age squared as control variables. Additionally, I control for gender to account for any potential differences in regime preferences or state employment.

## Descriptive Statistics on Post-Communist Countries 
Following the collapse of the Soviet Union and the subsequent transformation of communist regimes in European countries, free market economies and private businesses began to emerge and develop. However, even 15 years after the dissolution of the Soviet Union, the state remained a significant employer in many of these countries. 

![State employment](Data Visualizations/MapOfStateEmployement_2006.png)

The figure presents the average percentage of public employment in democratic and non-democratic countries in 2006. The data reveals that public employment constituted approximately 42% of total employment in democratic countries, compared to nearly 60% in non-democratic countries. Among non-democratic countries, Azerbaijan, Belarus, and Uzbekistan exhibited the highest shares of public employment at 75%, 74%, and 63%, respectively. In contrast, the Czech Republic, Hungary, and Latvia demonstrated the lowest shares at 30%, 31.5%, and 33%, respectively. Notably, Georgia and Ukraine, classified as on the verge of democracy in early 2006, displayed relatively higher shares of public employment at 58.5% and 51%, respectively, compared to other democratic countries.

The reasons for such considerable variations in the shares of public employment among countries are multifaceted. In some cases, such as Georgia, Bosnia and Herzegovina and Tajikistant (Pomfret, R., 2006), wars and political instability hindered the development of the private sector. In other instances, like Russia, inadequate protections and regulations failed to support a fair and transparent privatization process (Miller, 2018). On the other hand, European Union membership and a relatively stable political environment facilitated private sector development in countries including the Baltic states, Hungary, the Czech Republic, and Poland (Åslund, 2008).


