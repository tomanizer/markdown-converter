## Page 1
American Economic Review 2022, 112(4): 1194–1225
https://doi.org/10.1257/aer.20191823
Measuring Geopolitical Risk†
By Dario Caldara and Matteo Iacoviello*
We present a n ews-based measure of adverse geopolitical events and
associated risks. The geopolitical risk GPR index spikes around the
( )
two world wars, at the beginning of the Korean War, during the Cuban
Missile Crisis, and after 9 11. Higher geopolitical risk foreshadows
/
lower investment and employment and is associated with higher disas-
ter probability and larger downside risks. The adverse consequences
of the GPR index are driven by both the threat and the realization of
adverse geopolitical events. We complement our aggregate measures
with industry- and fi rm-level indicators of geopolitical risk. Investment
drops more in industries that are exposed to aggregate geopolitical
risk. Higher fi rm-level geopolitical risk is associated with lower
firm-level investment. JEL C43, E32, F51, F52, G31, H56, N40
( )
Entrepreneurs, market participants, and central bank officials view geopoliti-
cal risks as key determinants of investment decisions and stock market dynamics.
The Bank of England includes geopolitical risk, together with economic and pol-
icy uncertainty, among an “uncertainty trinity” that could have significant adverse
economic effects Carney 2016 . In recent years, the European Central Bank, the
( )
International Monetary Fund, and the World Bank have routinely highlighted and
monitored the risks to the outlook posed by geopolitical tensions.1 In a 2017 Gallup
survey of more than 1,000 investors, 75 percent of respondents expressed worries
about the economic impact of the various military and diplomatic conflicts happen-
ing around the world.2
From the standpoint of many economic models, adverse geopolitical events and
threats can impact macroeconomic variables through several channels, such as loss
of human life, destruction of capital stock, higher military spending, or increased
* Caldara: Board of Governors of the Federal Reserve email: dario.caldara@frb.gov; Iacoviello: Board of
( )
Governors of the Federal Reserve email: matteo.iacoviello@frb.gov. Emi Nakamura was the coeditor for this article.
( )
We thank Alessandra Bonfiglioli, Andrea Prestipino, Andrea Raffo, Bo Sun, Chris Erceg, Colin Flint, Nick Bloom,
Nils Gornemann, Ricardo Correa, Robert Engle, Steve Davis, as well as seminar and conference audiences. We are
grateful for the support from the GRUV Global Risk, Uncertainty, and Volatility network at the Federal Reserve
( )
Board and for the help from the staff of the Federal Reserve Board Research Library. We are grateful to the editor
and four referees for their helpful and constructive comments. Andrew Kane, Bethel Cole-Smith, Charlotte Singer,
Erin Markiewitz, Fatima Choudhary, Joshua Herman, Lucas Husted, Maddie Penn, Patrick Molligo, Sarah Conlisk,
and Theresa Dhin provided outstanding research assistance. All errors and omissions are our own responsibility. The
views expressed in this paper are solely the responsibility of the authors and should not be interpreted as reflecting the
views of the Board of Governors of the Federal Reserve System or of anyone else associated with the Federal Reserve
System. Updated data on geopolitical risk can be found at https://www.matteoiacoviello.com/gpr.htm.
† Go to https://doi.org/10.1257/aer.20191823 to visit the article page for additional materials and author
disclosure statements.
1 These institutions keep track of geopolitical risks using our index presented here.
2 See http://www.businesswire.com/news/home/20170613005348/en/.
1194

## Page 2
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1195
precautionary behavior. However, the importance of geopolitical factors in shaping
macroeconomic outcomes has not been the subject of systematic empirical analysis.
The main limitation has been the lack of an indicator that is consistent over time,
and that measures real-time geopolitical tensions as perceived by the press, the pub-
lic, global investors, and policymakers. This is the perspective we adopt here. We
construct newspaper-based indices of geopolitical risk GPR , daily and monthly,
( )
global and country-specific, and examine their evolution since 1900. Using aggre-
gate macroeconomic data, we then show that higher GPR increases the probabil-
ity of an economic disaster and predicts lower investment and employment. Using
firm-level data, we document that the adverse implications of geopolitical risk are
stronger for firms in more exposed industries, and that high fi rm-level GPR is asso-
ciated with lower firm-level investment.
The construction of our index consists of definition, measurement, and validation.
Section I presents definition and measurement. We define geopolitical risk as the
threat, realization, and escalation of adverse events associated with wars, terrorism,
and any tensions among states and political actors that affect the peaceful course of
international relations.3 In the measurement step, we draw on Saiz and Simonsohn
2013 and Baker, Bloom, and Davis 2016 , and construct the GPR index with
( ) ( )
an algorithm that computes the share of articles mentioning adverse geopolitical
events in leading newspapers published in the United States, the United Kingdom,
and Canada. These newspapers cover geopolitical events of global interest, often
implying an involvement of the United States. That said, while the GPR index can
be viewed either as a measure that is relevant for major companies, investors, and
policymakers, or as a measure that is mostly relevant from a North American and
British perspective, our validation analysis shows that our index can be further sliced
into separate country-specific components, likely reflecting the different geographic
imprint of major geopolitical events.
We plot the recent index, dating back to 1985, in Figure 1. The three largest
spikes are recorded during the Gulf War, after 9 11, and during the 2003 invasion of
/
Iraq. More recently, the index spikes after the Paris terrorist attacks and during the
2017–2018 North Korea crisis. We also construct the daily GPR index Figure 2 as
( )
well as the historical GPR index, dating back to 1900, which spikes at the beginning
of the two world wars, as well as around D -Day, the Korean War, and the Cuban
Missile Crisis Figure 3 . Elevated readings of the index reflect the realization or
( )
escalation of current adverse events, as well as expectations and threats about future
adverse geopolitical events. To quantify these two components, we construct the
geopolitical acts index and the geopolitical threats index, shown in Figure 4.
In Section II we present a variety of checks that verify the plausibility of the
GPR index and compare the index with related economic and geopolitical indi-
cators. In addition to performing a formal audit of a sample of 7,000 newspaper
articles, we verify that our automated index is highly correlated with a narrative
counterpart constructed by manually scoring the 44,000 front pages of the New York
Times published from 1900 through 2019. Moreover, we show that spikes in our
index and its components highlight w ell-known historical episodes associated with
3 The term “risk” is a bit of a misnomer, since it includes both the threat and the realization of adverse events.
Section I explains the rationale for our naming convention.

## Page 3
1196 THE AMERICAN ECONOMIC REVIEW APRIL 2022
wars, terrorism, or international crises. Based on these exercises and other robust-
ness checks, we conclude that the GPR index is meaningful and accurate.
In Sections III and IV, we look at the macroeconomic effects of geopolitical risk.
For the United States, using vector autoregressive VAR models for the period
( )
1985 to 2019, we find that a shock to geopolitical risk induces persistent declines
in investment, employment, and stock prices, with the decline in activity due to
both the threat and the realization of adverse geopolitical events. In addition, using
cross-country data and country-specific indices spanning 120 years, we find that
higher values of the GPR index are associated with i higher probability of eco-
( )
nomic disasters, ii lower expected GDP growth, and iii higher downside risks to
( ) ( )
GDP growth.
In Section V, we provide further evidence on the implications of geopolitical risk
using industry and firm-level data. The aggregate GPR index correlates well with
listed firms’ own perceptions of geopolitical risks, which we construct from men-
tions of geopolitical risks in 135,000 firms’ earnings calls, inspired by Hassan et al.
2019 . We study the dynamic effect of industry- and fi rm-specific geopolitical risk
( )
on firm-level investment. Industries that are positively exposed to geopolitical risks
suffer a decline in investment that is larger than the aggregate effect. Idiosyncratic
geopolitical risk—constructed using the transcripts of firms’ earnings calls, and
purged of aggregate and i ndustry-specific components—is associated with lower
investment at the firm level, with effects that accumulate and persist over time.
Our paper makes three contributions. First, we develop a new measure of adverse
geopolitical events. Around some key dates, the GPR index shares some of its spikes
with the military spending news variable of Ramey 2011 , with indicators of the
( )
human cost of conflicts, with the economic policy uncertainty EPU index of Baker,
( )
Bloom, and Davis 2016 , and with financial volatility. However, the GPR index
( )
also captures important information about geopolitical events that is not reflected in
these indicators. Second, we distinguish the threats of adverse geopolitical events
from their actual realization.4 We do so because our methodology pinpoints the
timing of different types of geopolitical events, thus allowing measurement of their
effects.5 Third, we present new systematic evidence on the role of adverse geopolit-
ical events in business fluctuations, using quarterly VARs, c ross-country historical
data, and firm-level data.
I. Construction of the GPR Indices
The construction of GPR indices involves definition, measurement, and valida-
tion. We first describe the definitions of geopolitics and geopolitical risk adopted in
our paper. We then discuss how we measure geopolitical risk and describe the key
features of the resulting indices.
4 A growing literature studies the distinction between expectations and realizations of macroeconomic and
financial phenomena. Bloom 2009 controls for the level of the stock market when identifying shocks to financial
( )
uncertainty. Berger, D ew-Becker, and Giglio 2019 find that expectations about future volatility are not contrac-
( )
tionary after controlling for current volatility.
5 Ludvigson, Ma, and Ng 2021 and Caldara et al. 2016 study the relationship between economic uncertainty
( ) ( )
and the business cycle by controlling for financial and economic activity when identifying uncertainty shocks. Our
emphasis on geopolitical risk also links our paper to the literature on disaster risk. See for instance Barro 2006;
( )
Gourio 2008; Berkman, Jacobsen, and Lee 2011; Pindyck and Wang 2013; and Nakamura et al. 2013.
( ) ( ) ( ) ( )

## Page 4
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1197
A. Definition of Geopolitical Risk
Formally, geopolitics is the study of how geography affects politics and the rela-
tions among states Foster 2006 and Dijkink 2009 . By contrast, the popular usage
( )
of the term geopolitics is more complex and contested, ranging from narrow to
broad definitions of what constitutes geography and who the relevant political actors
are. In A Dictionary of Human Geography, Rogers, Castree, and Kitchin 2013
( )
state that the media often refer to geopolitical concerns to describe the impact of
international crises and international violence. This is the perspective we adopt here.
We define geopolitical risk as the threat, realization, and escalation of adverse
events associated with wars, terrorism, and any tensions among states and political
actors that affect the peaceful course of international relations.
Two considerations about our definition are in order. First, our definition of
geopolitical builds on the historical usage of the term—to describe the practice of
states to control and compete for territory Flint 2016 . However, in line with recent
( )
assessments of modern international relations, our definition also includes power
struggles that do not involve acts of violence and competition over territories, such
as the Cuban Missile Crisis or recent tensions between the United States and Iran, or
the United States and North Korea. Our definition also includes terrorism. In recent
decades, terrorist acts have generated political tensions among states and, in some
instances, have led to full-fledged wars.
Second, our definition of geopolitical risk captures—with a slight abuse of the
word “risk”—a wide range of adverse geopolitical events, from their threat, to their
realization, to their escalation. This choice is dictated by journalistic practices and
measurement considerations. Regarding journalistic practices, in naming our index,
we followed a tradition in the media that refers to geopolitical risks as a catchall
phrase to describe the effects of international crises and violence, actual or perceived
Rogers, Castree, and Kitchin 2013 . Regarding measurement considerations, our
( )
extensive reading of news coverage on wars, terrorism, and international crises over
the past 120 years revealed that the threat, realization, and escalation of international
violence are often intertwined, so that a headline measure that abstracts from one
of these components may not capture the range of events that could be of interest to
researchers. That said, we break the headline index into separate “acts” and “threats”
components, so that interested researchers can choose their preferred components
for downstream empirical applications.
B. Measurement
Our sample is the text contained in about 25 million news articles published
in the print edition of leading English-language newspapers from 1900 through
the present, corresponding to about 30,000 and 10,000 articles per month in the
recent and historical sample, respectively. We construct the GPR index by count-
ing, each month, the share of articles discussing adverse geopolitical events and
associated threats. The recent GPR index starts in 1985 and is based on automated
text-searches on the electronic archives of 10 newspapers: the Chicago Tribune, the
Daily Telegraph, the Financial Times, the Globe and Mail, the Guardian, the Los
Angeles Times, the New York Times, USA Today, the Wall Street Journal, and the

## Page 5
1198 THE AMERICAN ECONOMIC REVIEW APRIL 2022
Washington Post. The choice of six newspapers from the US, three from the United
Kingdom, and one from Canada reflects our intention to capture events that have
global dimension and repercussions.6 The index counts, each month, the number of
articles discussing rising geopolitical risks, divided by the total number of published
articles. By the same token, the historical GPR index, dating back to 1900, is based
on searches of the historical archives of the Chicago Tribune, the New York Times,
and the Washington Post.
To construct our outcome of interest, we use a dictionary-based method, specify-
ing a dictionary of words whose occurrence in newspaper articles is associated with
coverage of geopolitical events and threats. Such a method organizes prior informa-
tion about how features of a text e.g., the occurrence in newspaper articles of the
(
words “war” and “threat” within close proximity map into the outcome of interest
)
e.g., news coverage of geopolitical risks . The use of supervised or unsupervised
( )
algorithms or p respecified dictionaries is less applicable to our case as the outcome
of interest is not directly observed and there are no readily available data to train a
supervised model.7
How do we specify the information that guides the construction of the dictionary?
First, we build directly on the definition of geopolitical risk adopted in this paper,
selecting words that closely align with our definition. Second, we use information
from two geopolitical textbooks and from the Corpus of Historical American English
to isolate themes that are more likely to be associated with geopolitical events such
(
as “war on terror” or “nuclear weapon” or words that are more likely to be used
[ ] )
in conjunction with war-related words such as “declare” . Third, we organize the
( )
search around h igh-frequency words and their synonyms that are more likely to
appear in newspapers on days of high geopolitical tensions see Tables A.1 and A.2
(
in the online Appendix . For instance, the word “crisis” has a relative term frequency
)
of 0.25 percent on days of high geopolitical tensions compared to 0.04 percent on an
average day. Words very likely to appear in newspapers on days of high geopolitical
tensions include “terror,” “blockade,” “invasion,” “troops,” and “war.”
Our goal is to provide an index that can highlight distinct aspects of geopolitical
risk, and that can be sliced conceptually and geographically. Doing so exclusively
with one-word searches would likely lead to misclassification and measurement
error. These considerations lead to our search query, which specifies two words
or phrases whose joint occurrence likely indicates adverse geopolitical events. The
query is described in Table 1, and is organized in eight categories see panel A .
( )
Each category is captured by a search query comprising two sets of words, the first
set containing topic words e.g., “war,” “nuclear,” or “terrorism” , the second set
( )
containing “threat” words for categories 1 through 5 and “act” words for categories
6 through 8. For six of our categories, we run proximity searches e.g., searching for
(
“terrorist” and “risk” appearing within two words of each other . For two catego-
)
ries, we search for either two words appearing in the same article “weapons” and
(
“blockade” or for one bigram and one word appearing in the same article “nuclear
) (
6 These newspapers have high circulation throughout the sample, consistent coverage of international political
events, and digital archives that span a long period. In Section II we verify that an index that excludes n on-US
newspapers is very similar to the benchmark index.
7 See Gentzkow, Kelly, and Taddy 2019 for a detailed comparison of methods for text analysis.
( )

## Page 6
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1199
Table 1—Search Query for the GPR Index
Contribution
to index percent
1900– 1960–
Category Search query Peak month Full sample 1959 2019
( )
Panel A. Search categories and search queries
Threats
1. War threats War_words N 2 Germany invades Czech. 13.5 17.9 9.2
/
Threat_words September 1938
( )
2. Peace threats Peace_words N 2 Iran crisis of 1946 3.5 4.3 2.7
/
Peace_disruption_words April 1946
( )
3. Military buildup Military_words AND Cuban Missile Crisis 23.5 21.3 25.8
buildup_words October 1962
( )
4. Nuclear threats Nuclear_bigrams AND Nuclear ban negotiations 10.1 4.2 16.0
Threat_words August 1963
( )
5. Terrorist threats Terrorism_words N 2 9 11 2.7 0.3 5.0
/ /
Threat_words October 2001
( )
Acts
6. Beginning of war War_words N 2 WWII begins 18.8 26.8 10.7
/
War_begin_words September 1939
( )
7. Escalation of war Actors_words N 2 D-Day 19.6 23.9 15.3
/
Actors_fight_words June 1944
( )
8. Terrorist acts Terrorism_words N 2 9 11 8.3 1.3 15.2
/ /
Terrorism_act_words September 2001
( )
Panel B. Search words
Topic sets Phrases
War_words war OR conflict OR hostilities OR revolution* OR insurrection OR uprising OR
revolt OR coup OR geopolitical
Peace_words peace OR truce OR armistice OR treaty OR parley
Military_words military OR troops OR missile* OR “arms” OR weapon* OR bomb* OR warhead*
Nuclear_bigrams “nuclear war*” OR “atomic war*” OR “nuclear missile*” OR “nuclear bomb*”
OR “atomic bomb*” OR “h-bomb*” OR “hydrogen bomb*” OR “nuclear test” OR
“nuclear weapon*”
Terrorism_words terror* OR guerrilla* OR hostage*
Actor_words allie* OR enem* OR insurgen* OR foe* OR army OR navy OR aerial OR troops
OR rebels
Threat act sets Phrases
/
Threat_words threat* OR warn* OR fear* OR risk* OR concern* OR danger* OR doubt* OR
crisis OR troubl* OR disput* OR tension* OR imminen* OR inevitable OR footing
OR menace* OR brink OR scare OR peril*
Peace_disruption_words threat* OR menace* OR reject* OR peril* OR boycott* OR disrupt*
Buildup_words buildup* OR build-up* OR sanction* OR blockad* OR embargo OR quarantine
OR ultimatum OR mobiliz*
War_begin_words begin* OR start* OR declar* OR begun OR began OR outbreak OR “broke out”
OR breakout OR proclamation OR launch*
Actor_fight_words advance* OR attack* OR strike* OR drive* OR shell* OR offensive OR invasion
OR invad* OR clash* OR raid* OR launch*
Terrorism_act_words attack OR act OR bomb* OR kill* OR strike* OR hijack*
Panel C. Excluded words
Exclusion words movie* OR film* OR museum* OR anniversar* OR obituar* OR memorial* OR arts
OR book OR books OR memoir* OR “price war” OR game OR story OR history OR
veteran* OR tribute* OR sport OR music OR racing OR cancer OR “real estate” OR
mafia OR trial OR tax
Notes: In panel A, the contribution to the index is the percent of articles in each category satisfying the condition
for inclusion in the GPR index, as a share of all articles satisfying that condition. In panel B, “core words” for each
category are highlighted in bold. The truncation character * denotes a search including all possible endings of a
( )
word, e.g. “threat*” includes “threat” or “threats” or “threatening.

## Page 7
1200 THE AMERICAN ECONOMIC REVIEW APRIL 2022
war” AND “threat” . We do plenty of robustness analysis around this search strat-
)
egy discussed in Section II and verify that, in our application, this approach yields
( )
better outcomes relative to a search using bigrams only, as in Hassan et al. 2019 ,
( )
or using Boolean operators only, as in Baker, Bloom, and Davis 2016 , who search
( )
“economic” and “policy” and “uncertainty” terms.
Panel B of Table 1 describes the sets of words constituting our dictionary. For
each category, we started from a minimal set of “core words,” denoted in red. For
instance, for category 1 the two core words are “war” and “conflict.” For category 2,
the core word is “peace.” For category 3, the core words are “military” and “troops.”
Core words that indicate threats are “threat,” “warn,” “fear,” “risk,” and “concern.”
These sets of words are the most common words used in news coverage to discuss
war-related threats. As shown in Section II, exclusive reliance on these core words,
while resulting in an index that shares a similar contour to our final index, would
lead to searches that fail to capture several articles that discuss geopolitical events
and risks. For this reason, we add words that are used throughout our historical
sample to cover multiple episodes. For instance, news coverage of military buildups,
embargoes, and sanctions such as during the Cold War, the Cuban Missile Crisis,
(
or the r un-up to the Gulf War relies on words that are not included in the core set.
)
Threats to peace are often referred to as “disruptions” of peace, a word that is not
used to directly indicate war threats. For the nuclear threats category, we use bigrams
to reduce the possibility that articles related to civilian usage of nuclear technologies
would slip into our search. Finally, the bottom panel lists “excluded words” that our
audit revealed to be more frequently associated with false positives. Articles that
mention these words cover a diverse set of topics, such as movies and books, sport
events, war anniversaries, and obituaries of famous generals and politicians. The
excluded words do not affect the spikes in our index. Nonetheless, accounting for
these words mitigates spurious trends and reduces the share of false positive articles
in the index see Table A.3 in the online Appendix .
( )
C. The Recent GPR Index
Figure 1 presents the GPR index from 1985 through 2020 based on ten news-
papers. The index is characterized by several spikes corresponding to key adverse
geopolitical events. The first spike is recorded in April 1986 and corresponds to
the terrorist escalation that led to the US bombing of Libya. The second spike hap-
pens around the Iraq invasion of Kuwait and the subsequent Gulf War. The index
surges at the beginning of 1993, during a period of escalating tensions between the
United States and Iraq. It then trends downwards until 2001 when it surges after
the 9 11 events, before spiking again during the 2003 invasion of Iraq. In recent
/
years, the index is high during the 2011 military intervention in Libya, around the
2014 Russian annexation of the Crimea peninsula, and after the 2015 Paris terrorist
attacks. The index displays a break in its mean after 2001. The 9 11 terrorist attacks
/
saw a shift in news coverage of geopolitical events, driven by increased reporting on
terrorist threats and on the war on terror.8
8 We perform a supremum Wald test for structural break at an unknown date using symmetric trimming of 15 per-
cent. We reject the null of no break in the log of the GPR index p -value of 0.001 and find a break in September
( < )

## Page 8
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1201
600 9 11
/
Iraq
400 Gulf War War
Iraq Paris
invades attacks
Kuwait US-North
Russia
Korea
annexes
200 US London Crimea tensions
bombing bombings
Libya Interv. US-Iran
Airstrikes Libya tensions
on Iraq
Bosnian
War
100
50
1985 1990 1995 2000 2005 2010 2015 2020
Figure 1. Recent GPR Index from 1985
Notes: Recent GPR index from 1985 through 2020. Index is normalized to 100 throughout the 1985–2019 period.
Figure 2 shows the GPR index at daily frequency. The daily index is noisier than
its monthly counterpart but provides a detailed view of a larger set of episodes,
including those that may seem to be missed by the monthly index. For instance, in
August 1991, the daily index captures the escalation of ethnic violence in the former
Yugoslavia, and the attempted coup in the Soviet Union. In March 1999, the index
spikes at the beginning of the North Atlantic Treaty Organization NATO air strikes
( )
in Kosovo. These events have a low bearing on the monthly index, as the associated
news coverage was short-lived.
The daily GPR index illustrates how the unfolding of geopolitical tensions can
add up to elevated values in its monthly counterpart. In a first scenario, a protracted
buildup in tensions leads to a defining event causing a big spike in the index, as
in the case of the Gulf War. In a second scenario, one climactic event causes a
large spike in daily geopolitical risk and is followed by readings that are persistently
higher than the average, as in the aftermath of the 9 11 terrorist attacks. In a third
/
scenario, s low-moving geopolitical tensions persistently remain in the news cycle,
averaging out to elevated values in the monthly GPR. Examples include the Syrian
Civil War and the 2017–2018 North Korea crisis. In all these scenarios, spikes in the
daily index correctly point to when tensions materialized, thus bolstering evidence
of the informative content that the index produces at daily frequencies. That said, it
is possible that our index may not appropriately measure episodes that slowly unfold
over multiple years, such as the fall of communism in the Soviet Union and Eastern
Europe, and are recognized as geopolitical risks only with the benefit of hindsight.
2001. Higher news coverage of geopolitical risks after 9 11 may indicate either an increase in actual risks of wars
/
and terrorism, or an increase in the public perception of these risks. An important question for future research would
be to study the relative importance of perceived versus actual geopolitical risks for economic outcomes.

## Page 9
1202 THE AMERICAN ECONOMIC REVIEW APRIL 2022
1985
1985 06 18: TWA hijacking
/ /
1986 04 16: US bombing of Libya
/ /
1987 1987 04 28: US-Russia negotiations over nuclear weapons
/ /
1987 10 10: War threats in Persian Gulf
/ /
1989
1989 12 21: US invades Panama
/ /
1990 08 08: Iraq threatens US Embassy
/ /
1991 1991 01 18: Gulf War. Iraq fires at Israel
1991 08 20: Coup in Soviet Unio/n /
/ /
1991 08 09: Ethnic violence in Yugoslavia
/ /
1993 1993 01 14: Air strikes against Iraq
/ /
1993 06 28: US raid on Baghdad
/ /
1994 02 08: NATO ultimatum to Serbia
/ /
1995
1996 09 04: US raid on Iraq
1997 / /
1998 02 24: US considers strike against Iraq
/ /
1999 1999 03 19 2 9 5 8 :/ B 1 e 2 g/ 1 in 8 n : i I n r g a q K d o i s s o a v r o m A a i m r W en a t r crisis escalation
/ /
1999 12 28: Holidays’ terrorist concerns
/ /
2001 2001 09 12: 9 11 Terrorist attacks
/ / /
2001 10 09: US invades Afghanistan
2002 09 27: War fears US Iraq / /
2003 / / / 2003 03 21: Beginning of the Iraq War
/ /
2004 03 23: Assassination of Sheik Yassin, Middle East tensions
/ /
2004 08 03: Terrorist threats in New York and Washington
2005 / /
2005 07 08: London bombings 7 7
/ / /
2006 08 11: Transatlantic aircraft plot
2007 2007 05 01: Wa / r a / nd terrorism concerns, protests in Turkey
/ /
2008 08 12: South Ossetian War escalation
2009 / /
2009 12 29: Flight 253 failed bombing attempt
/ /
2011 2011 05 03: US announces death of Osama Bin Laden
/ /
2013
2013 08 29: Escalation of Syrian Crisis
2014/ 03/ 04: Russia invades Crimea
201/4 0/9 01: Escalation Ukraine Russia
2015 / / /
2015 11 17: Paris terrorist attacks
/ /
2016 07 16: Turkish coup attempt
2017 / /
2017 08 22: North Korea tensions
/ /
2018 04 12: Syria missile strikes
/ /
2019
2020 01 07: US Iran tensions escalate
/ / /
0 200 400 600 800 1,000 1,200
Figure 2. Daily Geopolitical Risk
Notes: Timeline of the daily GPR index from 1985 through end-2020. The solid blue line plots the monthly index.
The green dots show the daily observations, including descriptions of the events reported by the newspapers
on selected days featuring spikes in the index shown by the large red dots. Index is normalized to 100 in the
( )
1985–2019 period.
D. The Historical GPR Index
Figure 3 displays the historical GPR index from 1900 onward. The historical
index closely mimics the recent index during the period 1985 to 2020 when their
coverage overlaps, with a correlation of 0.95. The historical GPR index is higher,

## Page 10
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1203
Pearl
500 WWI WWII Harbor D-Day
begins begins
WWI
escalation
400
911
/
300
Germany Iraq Gulf Iraq War
invades Korean Cuban invadesWar
Czechia War Missile Yom Kuwait
BerlinCrisis Kippur
Italy- Problem Six War Falklands
Boxer Ethiopia War Day War
200 Rebellion Suez War I A nv fg a h s a io n n
Russia- Shanghai Crisis Paris
Japan Incident terror
War Occupation Bosnian attacks
of Ruhr War
100
0
1900 1920 1940 1960 1980 2000 2020
Figure 3. Historical GPR Index from 1900
Notes: Historical GPR Index from January 1900 through December 2020. Index is normalized to 100 throughout
the 1900–2019 period.
on average, during the first half of the twentieth century see summary statistics in
(
Table A.3 in the online Appendix .
)
Perhaps unsurprisingly, the highest readings of the index coincide with the two
world wars. The index spikes at the onset of World War I and World War II and
remains persistently high during each war. The index declines rapidly at the end
of World War II only to rise again during the Korean War. The second half of the
twentieth century witnessed several geopolitical threats and crises. For instance,
the index spikes during the Suez Crisis, the Cuban Missile Crisis, the Six-Day War,
and the Falklands War. The index stays at relatively high levels from the 1950s
through the mid-1980s, a time when the threat of nuclear war and geopolitical ten-
sions between countries were more prevalent than actual wars. As discussed, since
the 2000s, terrorism, the Iraq War, and rising bilateral tensions dominate the index.
E. Geopolitical Threats and Geopolitical Acts
Throughout history, the realization of adverse geopolitical events has often been
the catalyst for increased fears about future adverse events. For instance, terrorist
attacks may increase the threat of future attacks or of a war. Our search query and
the resulting GPR index capture both the realization of adverse geopolitical events
a terrorist attack or the outbreak of a war , and threats about the future adverse
( )
events.

## Page 11
1204 THE AMERICAN ECONOMIC REVIEW APRIL 2022
We construct two components of the GPR index, the geopolitical threats GPT
( )
and the geopolitical acts GPA indices. The GPT index searches articles including
( )
phrases related to threats and military buildups categories 1 through 5 in Table 1 ,
( )
while the GPA index searches phrases referring to the realization or the escalation
of adverse events categories 6 through 8 in Table 1 . Figure 4 plots the two indices
( )
since 1900. The GPT and GPA indices have a correlation of 0.59 over the full sam-
ple, and of 0.45 from 1985 onward. Even if some spikes in the two indices coincide,
there is also independent variation that is better highlighted when examining partic-
ular historical episodes. The beginning of World War I appears largely unexpected.
Throughout the war, the GPA index remains elevated while the GPT index remains
subdued, although a spike in threats when the US severs diplomatic relations with
Germany in February 1917 is followed by the American entry into World War I
two months later. The buildup to World War II sees the GPT index rise amid news
coverage of the risk of war, for instance during the annexation of Czechoslovakia
by Nazi Germany, whereas the GPA index spikes at the beginning of the war, after
Pearl Harbor, and around D-Day. By contrast, the 1960s witnessed international cri-
ses captured by spikes in the GPT index that did not lead to wars such as the Berlin
Crisis and the Cuban Missile Crisis. The GPT index surges in 1990 in the r un-up
Gulf war. The GPA index spikes after 9 11 and at the beginning of the Gulf War.
/
Finally, the GPT index is high relative to its historical average during the recent
tensions between the US and North Korea and Iran.
II. Validation of the Index
This section presents three exercises aimed at ensuring the validity of our indi-
ces. First, we verify that the GPR indices provide a plausible quantification of the
historical and geographical evolution of geopolitical risks. Second, we compare the
indices with similar economic and geopolitical data. Third, we summarize the audit
process and additional accuracy checks.
A. Plausibility
Largest Spikes in the Historical Index.—Our first plausibility test relies on the
logic that jumps in the index must capture the most important geopolitical risks of
the past 120 years, in the way these risks were perceived by the contemporaries.9 We
calculate surprises in the index and in its two main subcomponents as the residuals
of a regression of the relevant monthly indices on three of their own lags.
Table 4 illustrates that the relative magnitude of the historical jumps in the index
is reasonable. The largest shocks capture w ell-known episodes of sizable increases
in the risk associated with wars, terrorism, or international crises. The five largest
shocks are the beginning of both world wars, 9 11, Pearl Harbor, and the onset
/
of the Korean War. Some of these events illustrate examples of shocks to both the
threat and act components of the index. Other shocks, such as the Cuban Missile
9 One example of a possible discrepancy between contemporaries’ perception of risks and ex post perception is
given by the Cuban Missile Crisis. With hindsight, it is reasonable to claim that the dangers posed by the crisis were
far greater than the contemporaries understood. See for instance Sherwin 2012.
( )

## Page 12
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1205
700 GPR threats GPR acts
600
500
400
300
200
100
0
1900 1920 1940 1960 1980 2000 2020
World War I World War II Early 1960s
600 WWI begins 800 Pearl Harbor D-Day 400 Cuban Missile Crisis
Berlin Problem
US enters war 600 WWII begins 300
400 Germany
400 invades 200
Czechia
Occupation
200 Vera Cruz 200 100
0 0 0
1913 1915 1917 1919 1938 1940 1942 1944 1961 1962 1963 1964
Gulf War 9 11 and Iraq War 2016−2020
/ 200
Kuwait invasion 500 9 / 11 US-Iran
300 Gulf War 400 150 US-North Korea
Iraq War
200 300 100
200
100 50
100
0 0 0
1989 1990 1991 1992 2001 2002 2003 2004 20162017201820192020
Figure 4. Geopolitical Threats and Geopolitical Acts
Notes: Geopolitical threats GPT and the geopolitical acts GPA indices. The GPT index is constructed by search-
( ) ( )
ing articles in categories 1 to 5 in Table 1. The GPA index is constructed by searching articles in categories 6 to 8 in
Table 1. Both indices are normalized to 100 in the 1 900–2019 period.
Crisis or the Gulf War, weigh more heavily on either component, showcasing the
independent role played by threats and acts in the construction of the index. For
example, the Cuban Missile Crisis ranks fourth among the largest threats within the
past 120 years despite its official duration of only 13 days and the lack of public
attention that it garnered within its first week.
Comparison with a Narrative GPR Index.—Traditionally, a newspaper’s front
page gives the reader a summary of the most important news event of the day in
order of importance, with editors always ready to break out big headlines for the

## Page 13
1206 THE AMERICAN ECONOMIC REVIEW APRIL 2022
Table 2—Largest Geopolitical Shocks since 1900
Month Rank GPR Shock Event
Panel A. Shocks to the GPR index
1914:4 15 145.2 84.5 Occupation of Vera Cruz
1914:8 1 472.3 341.5 WWI begins
1916:6 14 318.3 93.2 WWI escalation
1917:2 6 350.2 141.9 US severs Germany relations
1938:9 11 210.7 109.9 Germany occupies Czechia
1939:9 2 484.2 318.6 WWII begins
1941:12 3 447.5 245.7 Pearl Harbor
1944:6 12 473.2 107.9 D-Day
1950:7 5 242.4 143.5 Korean War
1962:10 8 228.1 121.2 Cuban Missile Crisis
1973:10 13 161.1 94.3 Yom Kippur War
1990:8 9 191.9 115.5 Iraq invades Kuwait
1991:1 7 250.4 126.4 Gulf War
2001:9 4 289.9 238.2 9/11
2003:3 10 244.6 110.2 Iraq War
Month Rank GPR threats Shock Event
Panel B. Shocks to the threats component of the GPR index
1914:8 1 432.6 279.2 WWI begins
1938:9 5 316.1 217.1 Germany occupies Czechia
1939:9 2 480.0 246.8 WWII begins
1962:10 3 376.6 234.0 Cuban Missile Crisis
1990:8 4 314.1 225.7 Iraq invades Kuwait
Month Rank GPR acts Shock Event
Panel C. Shocks to the acts component of the GPR index
1914:8 2 571.5 456.9 WWI begins
1939:9 1 560.0 463.0 WWII begins
1941:12 4 665.7 391.5 Pearl Harbor
1991:1 5 273.1 196.9 Gulf War
2001:9 3 457.5 403.4 9/11
Notes: The table lists the largest shocks to the GPR index and its components in the 1900–
( )
2019 sample. For this table, the shocks are constructed as the residuals of a regression of the
level of the relevant monthly index against its first three lags.
most important stories. As a second check for the plausibility of the index, we com-
pare it with a “narrative” index of adverse geopolitical events that we constructed
by reading and scoring the headlines of 44,000 front pages of the print edition of the
New York Times from 1900 through 2019.10
Together with a team of research assistants, we read all headlines above the fold
of the front page of the New York Times, and assign to each day a score of a 0, 1, 2, or
5 depending on whether no headline features rising or existing geopolitical tensions
score: 0 ; one headline, but not the lead headline, features GPR score: 1 ; the lead
( ) ( )
headline, but not a banner headline, features GPR score: 2 ; the banner headline
( )
features GPR score: 5 .11 The resulting narrative index places heavy weight on the
( )
10 The front page of the New York Times has changed dramatically over time. A typical front page in 1900
had four times as much text as today, as well as more articles. Early on, the subject in the front page was mostly
domestic and international politics. Today, the front page covers a larger variety of topics including finance, family,
technology, and medicine. See Rosenthal 2004. That said, the front page and its headlines have always directed
( )
the reader to the most important issues of the day.
11 The weights are chosen to be roughly proportional to the space taken by the headline across the page.

## Page 14
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1207
600 WWI
escalation Narrative GPR
D-Day
WWII Historical GPR
begins
WWI
begins
400
Gulf Iraq War
War
911
Korean /
War Cuban Fall of
Suez Missile SaigonFalklands
Russ W ia- a J r apan Italy- W Et a h r iopia Crisis Crisis War a t P t e t a a rr r c o i k s r s
200
0
1900 1920 1940 1960 1980 2000 2020
Figure 5. Narrative GPR Index
Notes: The narrative GPR index is constructed by reading all daily front pages of the New York Times since 1900
and scoring them as 0, 1, 2, or 5 depending on the intensity of news about adverse geopolitical events. Both indices
are normalized to 100 in the 1 900–2019 period.
importance of the article, as reflected by its placement in the newspaper, and ade-
quately captures the tone of the event. Additionally, the narrative index, not relying
on a preset list of words, is unlikely to be affected by changes in language over time.
The narrative index is plotted in Figure 5 alongside our automated one. The two
indices share very similar l ong-run trends and display a very high correlation of 0.86 ,
sharing very similar spikes during the world wars and in the wake of the Korean
War, the Gulf War, and 9 11. This positive correlation bolsters our confidence that
/
the automated index is an accurate measure of geopolitical risks. We consider the
automated index to be a better benchmark relative to the narrative for three main
reasons. First, the automatic index enhances transparency and replicability. Second,
the narrative index relies only on the front page articles of one newspaper thereby
rendering scaling up and maintenance costly. Third, the narrative index may suffer
more from mismeasurement due to limited f ront-page space e.g., major concurrent
(
events crowd out front-page space so other relevant events are pushed elsewhere
in the newspaper and ambiguity of historical records thereby requiring difficult
) (
judgment calls .
)
Country-Specific Measures of Geopolitical Risk.—We construct country-specific
measures of geopolitical risk by counting joint occurrences in newspapers of geo-
political terms and the name of the country or its capital or main city in question.
( )
For instance, the GPR index for Japan is the share of articles that meet the criterion
for inclusion in the GPR index and that contain the words “Japan” or “Tokyo.” The
geographical disaggregation permits a more granular assessment of the index, quan-
tifying exposure of countries to global risks and highlighting geopolitical episodes
that, while relevant for individual countries or regions, receive little weight in the
aggregate index. Importantly, the resulting indices, being constructed using three

## Page 15
1208 THE AMERICAN ECONOMIC REVIEW APRIL 2022
US newspapers, capture the US perspective on risks posed by, or involving, the
country in question.
Figure 6 plots country-specific GPR indices for selected countries. Most coun-
tries share exposure to common geopolitical events, most notably the two world
wars and, more recently, the Gulf War and Iraq War. That said, a few spikes are iso-
lated to specific countries or regions. After World War II, the United Kingdom was
involved in several international crises, ranging from the dispute with Egypt over
the Suez Canal to the war against Argentina for control over the Falkland Islands.
Germany faced a major crisis that culminated in the construction of the Berlin Wall
in 1961. Japan, Russia, and China were opposed in regional wars in the first half of
the twentieth century. Mexico and Korea were each embroiled in two major wars
that saw the direct involvement of the United States.
B. Comparison with Related Economic and Geopolitical Data
Comparison with News about Military Spending.—The top panel of Figure 7
compares the historical GPR index with Ramey’s 2011 measure of news about US
( )
military expenditures constructed from historical records. Ramey’s series reports the
present discounted value of expected changes in defense expenditures constructed,
akin to our measure, using news from Business Week and other newspaper sources.
The two measures are clearly related, with a correlation of 0.29 over the period 1900:II
to 2016:IV. The GPR index is above its historical mean in 15 out of the 16 instances
in which the military spending news variable is larger than 5 percent of GDP. The two
measures also display independent variation driven by spikes in the GPR index unre-
lated to US military spending see Figure A.1 in the online Appendix , such as during
( )
both world wars, throughout the Korean War, and in the years following 9 11.
/
Comparison with War Deaths.—Our index assumes that the propensity to dis-
cuss a phenomenon in newspapers can be seen as an ordinal measure of the inten-
sity of that phenomenon, and is monotonically increasing in the phenomenon itself.
Figure 7 shows that the GPR index is positively correlated with worldwide deaths
from conflicts, a cardinal, albeit crude, measure of the risks posed by armed con-
flicts. The correlation coefficient between the two measures is 0.82. War deaths cor-
relate more with GPR acts 0.83 than with GPR threats 0.46 . The GPR index and
( ) ( )
deaths from conflict surge together during the two world wars, but their correlation
weakens after the 1950s. Of note, the level of the GPR index has been higher almost
every year since the end of World War II compared to any year during the interwar
period, whereas deaths have stayed at relatively low levels. It is no surprise that the
level of the index appears permanently higher after the world wars made humanity
more attentive to the risks posed by armed conflicts.
Comparison with Proxies for Uncertainty and Granger Causality Tests.—Figure 8
compares the recent GPR index with two popular measures of uncertainty: the old
VIX a measure of stock market volatility based on the options on the Standard
(
and Poor’s 100 stock index and the news-based EPU index of Baker, Bloom, and
)
Davis 2016 . There are two periods where all three indices rise simultaneously: in
( )
1990–1991, around the time of the Gulf War, and in 2001, after the 9 11 terrorist
/

## Page 16
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1209
GPR United States GPR United Kingdom
WWI
20
10 WWII
WWI WWII
15 8
9/11 6
10 KoreaCuba Gulf Iraq
4 Suez Crisis Falklands Iraq
5 2
0 0
1900 1920 1940 1960 1980 2000 2020 1900 1920 1940 1960 1980 2000 2020
GPR Japan GPR Russia
8 Pearl Harbor 6 WWI Cuba
6 RUS-JPN Hiroshima 4 RU W S- a J r PN WWII K Y W ip o p a m u r r Afghan Inv.
4 War Shanghai Inc. Revolution Gulf War Ukraine Annex.
WWI Korean War 2
2
0 0
1900 1920 1940 1960 1980 2000 2020 1900 1920 1940 1960 1980 2000 2020
GPR Germany GPR Korea
15 8
WWI Korean War
WWII 6
10 D-Day
4
5 Berlin Crisis 2 Flight007 Nucl.Crisis
0 0
1900 1920 1940 1960 1980 2000 2020 1900 1920 1940 1960 1980 2000 2020
GPR Mexico GPR China
Carrizal 4 Korean War
4 McArthur Inquiry
Vera Cruz Sino-Jap.
3 3 War Shanghai Inc. Ind W o- a P r ak.
2
2 Revolution
1 Huerta Rebell. 1 Tienanmen
0 0
1900 1920 1940 1960 1980 2000 2020 1900 1920 1940 1960 1980 2000 2020
Figure 6. Country-Specific Geopolitical Risk
Note: For each country, the country-specific GPR index measures share of articles simultaneously mentioning geo-
political risks together with the name of the country or its capital or main city in question.
( )
attacks. However, in both cases it seems plausible to argue that the causation runs
from geopolitical events to stock market volatility and policy uncertainty. The three
indices also exhibit sizable independent variation. The GPR index does not move
during periods of economic and financial distress or around presidential elections,
periods characterized by elevated policy uncertainty. By contrast, rises in the EPU
index and VIX do not coincide with the Russian annexation of Crimea or with ter-
rorist events other than 9 11. In sum, the graphical evidence indicates that, com-
/
pared to the VIX and the EPU index, the GPR index appear to capture—because
of its own nature—events that i are less likely to have an economic origin, and
( )
ii could give rise to heightened financial volatility and policy uncertainty.12
( )
12 In online Appendix B.10, we compare the GPR index to other quantitative proxies: International Crisis
Behavior ICB database, the national security EPU subindex, and the US external conflict rating index.
( )

## Page 17
1210 THE AMERICAN ECONOMIC REVIEW APRIL 2022
80 400
Mil. news percent of GDP, left scale
( )
60 GPR quarterly, right scale
( ) 300
40
200
20
100
0
20 0
−
1900:I 1920:I 1940:I 1960:I 1980:I 2000:I 2020:I
350 400
War deaths per 100,000, left scale
300 ( )
250 GPR ( annual ) , right scale 300
200
200
150
100 100
50
0 0
1900 1920 1940 1960 1980 2000 2020
Figure 7. Comparisons with Military Spending News and War Deaths
Notes: In the top panel, comparison of quarterly GPR index with the expected military spending news variable from
Ramey 2011, updated in Ramey and Zubairy 2018. In the bottom panel, comparison of the annual historical
( ) ( )
GPR index with worldwide military and civilian death rate from conflicts and terrorism see online Appendix B.4
(
for data sources.
)
600 80
GPR, left scale
400 VIX, right scale
60
200
40
100
20
50
0
1985 1990 1995 2000 2005 2010 2015 2020
600 400
GPR, left scale
400
EPU, right scale
300
200
200
100
100
50
0
1985 1990 1995 2000 2005 2010 2015 2020
Figure 8. Comparison with Financial and Economic Uncertainty Measures
Note: Comparison of the GPR index plotted on a log scale with financial volatility as measured by the Chicago
( )
Board Options Exchange’s Volatility Index old VIX, also known as VXO and with the economic policy uncer-
( )
tainty EPU index constructed by Baker, Bloom, and Davis (2016).
( )

## Page 18
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1211
Online Appendix B.5 shows that the GPR index is not Granger caused by news
related to recent developments in the United States. We regress the log of the GPR
index on macroeconomic variables change in US industrial production, private
(
employment, and the log of the West Texas Intermediate WTI price of oil deflated
( )
by the US consumer price index , financial variables real returns on the S&P 500
) (
index and the two-year Treasury yield , and proxies for uncertainty the VIX and the
) (
log of the EPU index . Macroeconomic, financial, and uncertainty developments do
)
not Granger cause the GPR index.
C. Additional Checks
Audit.—We evaluate the GPR index against alternatives based on different search
queries and we perform an extensive human audit of newspaper articles likely dis-
cussing geopolitical risks.
In the first exercise, we use the narrative index—constructed using the New York
Times front pages as discussed in Section IIA—as a reference point for assessing the
accuracy of the benchmark index. Specifically, we compare the benchmark index with
three alternatives based on slight modifications of the search query of Table 1. The
alternative indices i do not remove the “excluded words” from the query; ii are
() ( )
based on a smaller set of “core words”; iii use the Boolean operator “AND” for all
( )
search categories as opposed to a search of terms within two words from each other .
( )
We find that the GPR index exhibits a higher correlation with the narrative index than
the three alternative indices see online Appendix Table A.3 for details . Additionally,
( )
for each index, we randomly sample a large number of articles, read each of them, and
manually code them as either discussing high or rising geopolitical tensions or not. We
find the GPR index has a lower t ype I error rate relative to all alternatives.13
In the second exercise, we follow the approach of Baker, Bloom, and Davis
2016 and evaluate the GPR index through a human audit that further confirms the
( )
validity of the article selection process. The GPR index has a correlation of 0.93—at
an annual frequency—with a “human” GPR index that is constructed by manually
reading and coding a sample of more than 7,000 newspaper articles see online
(
Appendix B.6 for additional details .14
)
Are Results Sensitive to the Use of Different Newspapers?—The recent and histor-
ical GPR indices rely on ten and three newspapers, respectively. This choice avoids
reliance on one particular news source and provides a robust and stable account of
geopolitical risks. We find that the exact number of newspapers has only a modest
effect on the index see also online Appendix A.2 . The correlation between the
( )
historical index and the recent index is 0.95 for the period in which the two indices
overlap. Additionally, the correlation between n on-US and US newspapers’ GPR
is 0.88, thus suggesting that the global nature of most geopolitical events receives
similar coverage across US and n on-US newspapers. Finally, the Cronbach alpha, a
13 The GPR index trends slightly downward from 1900 onward, a plausible feature given the two world wars and
the Korean War in the early part of the sample.
14 Saiz and Simonsohn 2013 list a number of formal conditions that must hold to obtain useful document
( )
frequency-based proxies for variables and concepts that are otherwise elusive to measure, such as ours. In online
Appendix B.9, we show that our index satisfies the Saiz and Simonsohn 2013 conditions.
( )

## Page 19
1212 THE AMERICAN ECONOMIC REVIEW APRIL 2022
measure of internal consistency across indices based on the ten individual newspapers,
is 0.96, a number that indicates an excellent degree of reliability of our measure.
Does War Language Change over Time?—The construction of our index relies on
an extensive analysis of the most common words and sentences used in newspapers
over time to describe risks of war and risks to peace, and acts of war and terror. We
offer a detailed description of this analysis in online Appendix B.7, where we confirm
that we neither ignore nor o ver-rely on words used relatively more often in some
historical periods. First, we verify that we do not omit any crucial, w ar-related words
that are used relatively frequently in newspapers during selected episodes of elevated
geopolitical tensions. In particular, words such as terrorism, blockade, invasion, war,
crisis, troops, and threat, among others, have odds of appearing in newspapers on days
of high geopolitical risk that are at least five times higher relative to any average day
see online Appendix Table A.1 . Second, we analyze term frequency for the words
( )
and word combinations used to construct the index and study their evolution over
time. Online Appendix Tables A.4 and A.5 confirm that our query includes both words
that are more frequent in the early part of the twentieth century, such as “menace” or
“peril,” and words that are more frequent in recent decades, such as “risk” or “tension.”
As a final consideration, we recognize that newspapers appear to have devoted
increasingly more space to arts, history, sports, and entertainment, often borrowing
some of their language from warfare and military terminology. For this reason, our
search ignores the articles containing the “excluded words” of Table 1. Without
these words, the index would have a slight upward trend throughout the historical
period, and slightly higher measurement error see online Appendix Table A.3 .
( )
Does Media Attention Measure the Underlying Risk?—An implicit hypothesis
of our analysis is that the propensity to mention geopolitical risks in newspapers
is representative of such propensity in the wider population. While a formal test of
this hypothesis would be beyond the scope of this paper, our online Appendix pro-
vides evidence that the GPR index is not unduly affected by issues related to how
the media reports the news. First, we show that the index is not prone to spurious
fluctuations when geopolitical events could be crowded out by unpredictable or pre-
dictable newsworthy events—from natural disasters to inflation to Olympic Games
to presidential elections see Figure A.4 and Table A.6 in the online Appendix .
( )
Second, we verify that our index is not impacted by the political orientation of the
newspapers used in the analysis see online Appendix Figure A.3 . Finally, we show
( )
that there is a high correlation between occurrence and extent of murders, hijack-
ings, and nuclear tests on the one hand, and the media coverage of these events on
the other. This correlation suggests that, even if these events share with geopolitical
news an alarmist message that may sell more newspapers, their occurrence is in line
with the media coverage see online Appendix Figure A.4 .
( )
III. VAR Evidence on the Effects of Geopolitical Risk
In this section, we present our investigation of the relationship between the GPR
index and aggregate economic activity in the United States using VAR models for
the period 1985 to 2019.

## Page 20
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1213
A. Aggregate Economic Effects
We examine the macroeconomic consequences of innovations to geopolitical
risk using a structural VAR model details and robustness analysis are in online
(
Appendix C . Our main specification, which we estimate using two lags and quar-
)
terly data from 1986:I through 2019:IV, consists of eight variables: i the log of the
( )
GPR index; ii the VIX; iii the log of real business fixed investment per capita;
( ) ( )
iv the log of private hours per capita; v the log of the S&P 500 index; vi the log
( ) ( ) ( )
of the WTI price of oil; vii the yield on t wo-year US Treasuries; viii the Chicago
( ) ( )
Federal Reserve’s National Financial Conditions Index NFCI .15
( )
We identify a GPR shock by using a Cholesky decomposition of the covariance
matrix of the VAR reduced-form residuals, ordering the GPR index first. The order-
ing implies that any contemporaneous correlation between economic variables and
the GPR index reflects the effect of the GPR index on the economic variables, rather
than the other way around. The characteristics of the GPR index discussed in the pre-
vious two sections lend support to this assumption. We explore robustness to alter-
native identification assumptions and VAR specifications in the online Appendix.
The solid lines in Figure 9 show the median impulse responses to a two standard
deviation shock to the GPR index.16 The size of the shock reflects the average of
the innovations in the right 10 percent tail of the GPR shock distribution. The GPR
index rises persistently and remains elevated for nearly two years. High geopolitical
risk is followed by a short-lived increase in financial uncertainty as measured by
the VIX, by a decline in stock prices and oil prices, and by a modest decrease in
the two-year yield. Fixed investment gradually declines, bottoming out at negative
1.5 percent after about one year, before slowly reverting to trend. Labor market
conditions deteriorate, with hours declining 0.6 percent one year after the shock.
The decline in investment and hours in the wake of a GPR shock is broadly consis-
tent both with models that emphasize the contractionary effects of future negative
news about the future—as in Beaudry and Portier 2006 and Jaimovich and Rebelo
( )
2009 —and with models where recessions are driven by shocks with a negative
( )
first moment and a positive second moment—such as Bloom et al. 2018 .17
( )
B. Acts and Threats
Next, we evaluate the difference between innovations in the two broad compo-
nents of the GPR index, the GPA index geopolitical acts and the GPT index geo-
( ) (
political threats . We modify the benchmark VAR by replacing the GPR index with
)
the GPA and GPT indices, using a Cholesky ordering with the GPA and GPT indices
ordered first and second, respectively. This ordering captures a specific configura-
tion of shocks such that “GPA shocks” can prompt a contemporaneous comovement
15 The stock market index and oil prices are divided by the Consumer Price Index for All Urban Consumers.
16 Figure A.6 in the online Appendix plots the estimated shocks to the GPR index and to its components both
for the VAR specification of this subsection and the VAR specification of Section IIIB.
17 When we add GDP to the VAR, we find that GDP drops 0.3 percent over the first year in response to a two
standard deviation geopolitical risk shock see online Appendix Figure A.7.
( )

## Page 21
1214 THE AMERICAN ECONOMIC REVIEW APRIL 2022
50
40
30
20
10 0
0 4 8 12
Quarters
Figure 9. The Impact of Increased Geopolitical Risk
Notes: The black solid line depicts the median impulse response of the specified variable to a two standard devia-
tion increase in the GPR index. The dark and light shaded bands represent the 68 percent and 90 percent pointwise
credible sets, respectively.
in acts and threats, whereas “GPT shocks” capture threats that do not immediately
materialize, leaving acts unchanged within the month.18
The solid lines in Figure 10 plot the median responses to the GPA and GPT
shocks. A shock to acts leads to a sharp and significant increase in threats, whereas
shocks to threats lead to a small and short-lived increase in acts. GPA and GPT
shocks induce similar declines on investment and hours, though the effects of GPA
shocks are more persistent.
To better quantify the role of acts and threats in affecting macroeconomic vari-
ables, we construct a counterfactual set of impulse responses for the two VAR
shocks in which threats are held constant in response to act shocks, and vice versa.
Specifically, in response to the GPA and GPT shocks, we select a sequence of GPT
and GPA shocks that hold GPT and GPA constant, respectively. The dashed lines
in Figure 10 illustrate that both acts and threats in isolation produce contractionary
effects. Were threats to remain unchanged in response to an acts shock, the response
of investment and hours would be smaller, thus supporting the notion that unre-
alized threats about future events could have contractionary effects. This result is
corroborated by the decline in activity associated with increases in threats, keeping
acts unchanged.
The contractionary consequences of the threats of adverse events support the
insights of theoretical models where agents form expectations using a worst case
18 An alternative identification scheme in which “threats” are ordered before “acts” would have the unpalatable
property that both GPT and GPA shocks move the GPA on impact, thus making it difficult to isolate historical events
when the threat component of the index moves substantially without a contemporaneous movement in acts, such as
the Cuban Missile Crisis or the recent United States-North Korea and United States-Iran tensions.
tnecreP
GPR
3
2
1
0
1 − 2 −
3
− 0 4 8 12
Quarters
xednI
VIX
2
0
2 −
4
− 0 4 8 12
Quarters
tnecreP
Private fixed
investment
1
0.5
0
0.5
− 1 −
1.5
− 0 4 8 12
Quarters
tnecreP
Hours
0
5 −
10
− 0 4 8 12
Quarters
tnecreP
S&P 500
10
5
0
5 −
10
−
15
− 0 4 8 12
Quarters
tnecreP
Oil price
0.5
0
0.5
− 0 4 8 12
Quarters
stniop
egatnecreP
Two-year yield
0.2
0.1
0
0.1
−
0.2
− 0 4 8 12
Quarters
xednI
NFCI index

## Page 22
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1215
Panel A. Impulse responses to a GPA shock
60
40
20
0
0 4 8 12
Quarters
Panel B. Impulse responses to a GPT shock
Figure 10. The Impact of Increased Geopolitical Risk: Acts versus Threats
Notes: The black line depicts the median impulse response of the specified variable to a two standard deviations
exogenous increase in the GPA index panel A and in the GPT index panel B. The red dashed line depicts the
( ) ( )
outcome of a counterfactual simulation that keeps GPT panel A and GPA panel B constant. The dark and light
( ) ( )
shaded bands represent the 68 percent and 90 percent pointwise credible sets, respectively.
probability, as in Ilut and Schneider 2014 , or models where the threat of adverse
( )
events leads agents to reassess macroeconomic tail risks, as in Kozlowski, Veldkamp,
and Venkateswaran 2018 . Of course, these findings may well depend on the coun-
( )
try and the period that are studied in our VAR. With the notable exception of 9 11,
/
most adverse geopolitical events in the sample did not directly hit the United States.
By contrast, it is well known that countries experiencing adverse geopolitical events,
wars in particular, on their soil suffer very large drops in economic activity, as doc-
umented by Barro 2006 and Glick and Taylor 2010 . We return to this theme in
( ) ( )
the next section.
IV. Tail Effects of Geopolitical Risk
In this section, we quantify the relationship between geopolitical risk a
(
noneconomic risk and risks to economic activity. We first show that high geopoliti-
)
cal risk is associated with a higher probability of economic disasters. We then show,
using quantile regressions, that elevated geopolitical risk is associated with lower
expected GDP growth and higher downside risks to GDP growth. We exploit varia-
tion in geopolitical risks and economic activity over time and across nations, using
annual data for 26 countries for the period 1900 to 2019. We measure geopolitical
tnecreP
GPR acts GPR threats
2
0
2
−
4
0 4 8 12 − 0 4 8 12
Quarters Quarters
Act shock Act with fixed threat
xednI
Private fixed
investment
1
0.5
0
0.5 −
1
−
1.5
− 0 4 8 12
Quarters
0 4 8 12 0 4 8 12 0 4 8 12 0 4 8 12
Quarters Quarters Quarters Quarters
tnecreP
Hours
Private fixed
GPR acts GPR threats investment Hours
60
40
20
0
tnecreP
60
40
20
0
tnecreP
60
40
20
0
tnecreP
2
0
2
−
−4
xednI
1
0.5
0
0.5 −
1
−
−1.5
tnecreP
Threat shock Threat with fixed acts

## Page 23
1216 THE AMERICAN ECONOMIC REVIEW APRIL 2022
risk using both the historical GPR index and the c ountry-specific indices described
above. The main advantage of using the c ountry-specific indices is to exploit epi-
sodes of higher geopolitical risk that are important for individual countries but that
receive a low weight in the aggregate index. For instance, c ountry-specific geopo-
litical risk is extraordinarily high for Korea in the 1950s, for Chile in 1973, and for
Argentina and Peru in 1982, all of which are episodes that saw foreign involvements
and that contributed to geopolitical tensions in Asia and South America.
A. Effects on Disaster Probability
We model the occurrence of disaster D in country i in year t as given by
i,t
1 D GPR GPRC GDP controls u ,
( ) i ,t = α i + β t + γ i ,t + δΔ i ,t − 1 + + i ,t
where D is a zero or one dummy for an economic disaster, is a country-fixed
i ,t αi
effect, GPR is the “global” GPR index, G PRC is the c ountry-specific index, and
GDP is real GDP growth. To measure D , we use the disaster dummy constructed
Δ i,t
in Nakamura et al. 2013 using an approach that generates endogenous estimates
( )
of the timing and length of an economic disaster. We update their estimation with
data through 2019.19
The first five columns of Table 3 show results from different specifications of
equation 1 . All models are estimated using a linear probability specification to
( )
simplify the interpretation of the coefficients, but the results are largely unchanged
when using a logistic specification. The simplest specification in column 1 has no
country-fixed effects and does not control for c ountry-specific risk. The coefficient on
global GPR is economically large. It indicates that a one standard deviation increase
in global geopolitical risk increases the probability of disaster by 18 percentage
points.20 Column 2 adds country fixed effects as well as c ountry-specific GPR. After
controlling for global factors, a o ne standard deviation rise in country-specific GPR
increases the disaster probability by 9 percentage points. Column 3 illustrates the
important role played by the two world wars in driving the relationship between
the global GPR and disaster probability. When the world war dummies are added
( )
to the specification, the coefficients on both global GPR index and war dummies
( )
are positive but not statistically significant, while the impact of country-specific
GPR remains large and significant. While many economic disasters of the twentieth
century took place during the two world wars, geopolitical risks and the associated
economic consequences materialized through history and across countries.
Column 4 replaces GPR with a variable measuring spikes in the index with nearly
unchanged results. Column 5 controls for US military spending news and allows for
a common shift in the disaster probability across three subsamples, as in Nakamura
19 We use the codes in Nakamura et al. 2013 to extend the estimation of the disaster events through 2019.
( )
Our procedure reproduces their disaster dates almost exactly, with a tetrachoric correlation coefficient between our
disaster dummy and theirs of 0.99. China and Russia are not part of their sample, but we include them for their role
in the geopolitical events of the period. We define disaster years in China as the periods 1940–1946 and 1960–1968.
We define disaster years in Russia as the periods 1914–1920, 1941–1945, and 1990–1995.
20 The share of disaster events in the sample is 17 percent. Sample average GDP growth is 2.9 percent in the
nondisaster state, 0.2 percent in the disaster state.
−

## Page 24
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1217
Table 3—Geopolitical Risk and Economic Disasters
Disaster Disaster Disaster Disaster Disaster Onset Ending
1 2 3 4 5 6 7
( ) ( ) ( ) ( ) ( ) ( ) ( )
GDP growth t-1 0.0071 0.0062 0.0056 0.0065 0.0056 0.0009 0.0012
− − − − − −
0.0030 0.0030 0.0030 0.0032 0.0026 0.0010 0.0010
( ) ( ) ( ) ( ) ( ) ( ) ( )
GPR 0.1753 0.1144 0.0337 0.1001 0.0180 0.0175
−
0.0223 0.0241 0.0469 0.0236 0.0237 0.0094
( ) ( ) ( ) ( ) ( ) ( )
Country GPR 0.0940 0.0842 0.0794 0.0664 0.0090
−
0.0160 0.0170 0.0175 0.0295 0.0105
( ) ( ) ( ) ( ) ( )
Dummy WWI WWII 0.3328
/
0.1761
( )
GPR spikes 0.1692
0.0246
( )
Country GPR spikes 0.0821
0.0122
( )
Dummy pre-1946 0.2437
0.0490
( )
Dummy 1946–1972 0.1152
0.0467
( )
Constant 0.2309 0.2289 0.1947 0.1762 0.1112 0.0401 0.1180
0.0252 0.0273 0.0341 0.0302 0.0320 0.0185 0.0130
( ) ( ) ( ) ( ) ( ) ( ) ( )
Observations 3,056 3,056 3,056 3,056 3,056 2,447 609
R2 0.20 0.20 0.21 0.18 0.26 0.13 0.02
Countries 26 26 26 26 26 26 26
Country fixed effects No Yes Yes Yes Yes Yes Yes
Notes: Standard errors in parentheses are clustered by country and year. The table shows the effects of global and
country-specific geopolitical risk on the probability of economic disaster in a panel of countries from 1900 through
2019. GDP growth is expressed in percent. GPR is standardized. Country GPR is standardized by country. Country
GPR is the number of GPR articles mentioning the country divided by total number of newspaper articles. The GPR
spikes variable equals GPR in the ten observations with the highest value of the GPR relative to a 20-year lagged
moving average, and zero otherwise. The country GPR spikes variable equals country GPR when country GPR
is larger than two standard deviations relative to a 20-year lagged moving average, and zero otherwise. The war
dummy equals one in the years 1914–1918 and 1939–1945. See online Appendix D for the list of countries. Disaster
episode data were constructed using updated GDP and consumption per capita data from Barro and Ursúa 2012
( )
and the methodology described in Nakamura et al. 2013.
( )
et al. 2013 : one before 1946, one for the period 1946 to 1972, and one for the
( )
period since 1973. The association of geopolitical risk with occurrence of disaster is
only slightly attenuated. Finally, in columns 6 and 7 we follow the approach in Bazzi
and Blattman 2014 , replacing the disaster dummy with a dummy equal to one
( )
either at the onset or at the end of a disaster, and zero otherwise.21 Column 6 shows
that disasters are more likely to start, rather than occur and persist, at times of high
geopolitical risk. A o ne standard deviation increase in c ountry-specific geopolitical
risk brings the probability of disaster onset from its historical mean of about 2.2
percent to 9 percent, an increase of 6.8 percentage points. Column 7 shows that high
geopolitical risk also reduces the probability of the ending of a disaster, though the
effects are smaller and more imprecise.
21 The onset disaster dummy is one when D D 1 and D 0 , zero in n ondisaster years, and
missing when both D 1 and D 1 Th e i , e t n − d i ng i ,t −o 1 f a = d isaster d u i, m t −m 1 y = t reats all disaster years as zero, the
year of the ending o f a i ,t d = isa ster as on i,t e−, 1 a n = d all other years as missing.

## Page 25
1218 THE AMERICAN ECONOMIC REVIEW APRIL 2022
The evidence in this subsection supports the idea that, historically, changes in
geopolitical risk are associated with substantial variations in the probability of large
declines in economic activity. Many economic disasters of the twentieth century
took place during the world wars, the two global events in our sample. However, our
estimates also demonstrate that regional and c ountry-specific geopolitical events
were associated with major economic crises.
B. Quantile Effects of Geopolitical Risk
Throughout history, wars have at times destroyed human and physical capital,
shifted resources from productive to less productive uses, and diverted international
trade. At other times, wars have enabled larger labor force participation, better tech-
nological diffusion, and larger infrastructure spending see Stein and Russett 1980 .
( )
We use c ross-country data and quantile regressions to evaluate how geopolitical risk
is associated with the distribution of future economic growth. Suppose for instance
that conflict is followed in some cases by faster, in some cases by slower growth,
like in the United States and Germany during World War II, respectively. If that is
the case, geopolitical risks may be associated with different outcomes at the low and
high ends of the GDP growth distribution. To test this hypothesis, we run quantile
regressions of the following form:
2 y x GPRC
( )  τ (Δ i ,t + 1 | i ,t ) = ατ + βτ i ,t .
Above, we estimate the best linear predictor of the quantile of variable y
τ Δ i,t + 1
one year ahead, conditional on values of country-specific geopolitical risk, denoted
by GPRC the regressions also control for global geopolitical risk . As dependent
i,t ( )
variables, we consider GDP growth, total factor productivity TFP growth, and
( )
military spending as a share of GDP. We estimate equation 2 at different quantiles.
( )
Table 4 shows the results. The ordinary least squares OLS estimates show that
( )
a rise in c ountry-specific GPR predicts lower expected GDP growth, lower expected
TFP growth, and higher expected military spending. The median effects row labeled
(
q50 have the same sign as the OLS estimates, though they are slightly smaller in
)
magnitude, suggesting that the effects of GPR are somewhat larger during a crisis. The
rows labeled q10 and q90 estimate equation 2 at the tenth and ninetieth quantiles.
( )
In line with the findings from the disaster risk regressions, a rise in the GPR index
increases the probability of particularly adverse economic outcomes. The left tail of
the GDP distribution, measured by the tenth quantile coefficient, shows a decline that
is four times larger than the OLS effect, whereas the right tail of the distribution,
measured by the ninetieth quantile, slightly increases. The conditional distributions of
one-year-ahead TFP growth displays higher uncertainty, with both positive and nega-
tive tail events becoming more likely. Finally, the right tail of military spending moves
disproportionally: elevated GPR predicts a risk of a large military buildup.
V. Geopolitical Risk and Firm-Level Investment
In our last step, we provide evidence on the effects of geopolitical risk on invest-
ment using fi rm-level data. There are two questions that we are interested in. First,

## Page 26
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1219
Table 4—Quantile Regression Effects of Country-Specific Geopolitical Risk
GDP growth t 1 TFP growth t 1 Military exp. t 1
(+ ) (+ ) (+ )
1 2 3
( ) ( ) ( )
OLS 0.35 0.22 2.15
− −
0.22 0.27 0.39
( ) ( ) ( )
Quantile
q50 0.24 0.04 0.63
− −
0.22 0.14 0.19
( ) ( ) ( )
q10 1.44 1.86 0.16
− −
0.63 0.45 0.03
( ) ( ) ( )
q90 0.30 1.53 7.08
0.30 0.55 0.55
( ) ( ) ( )
Observations 3,082 2,261 2,681
Countries 26 19 26
Notes: Standard errors, in parentheses, are bootstrapped using 500 replications. The table
shows quantile regression effects of geopolitical risk in a panel of countries from 1900 through
2019. In each specification, the right-hand side variable in country-specific GPR in year t
standardized by country. The dependent variables are GDP growth, TFP growth, and mili-
( )
tary expenditures in year t 1, respectively. GDP growth and TFP growth are expressed in per-
+
cent units. Military expenditures are expressed as a share of GDP. The OLS coefficients are
reported in the top row. The quantile coefficients report the effects at the fiftieth, tenth, and
ninetieth percentile of the distribution of the dependent variable. All regressions include an
intercept and control for global geopolitical risk. Real GDP per capita data are from Barro and
Ursúa 2012, extended through 2019 using the World Bank World Development Indicators.
( )
TFP data are from Bergeaud, Cette, and Lecat 2016. Military expenditures are taken from
( )
Roser and Nagdy 2013.
( )
do firms in industries more exposed to aggregate geopolitical risks experience a
larger decline in investment? Second, are idiosyncratic geopolitical events at the
level of the firm associated with fluctuations in investment?
A. Measuring Geopolitical Risk across Firms and Industries
It is useful to think of firm-level geopolitical risk as embedding three components:
3 GPR GPR GPR Z ,
( ) i ,t = t + t Λk + i ,t
where the subscripts i and k denote firms and industries, respectively. The first com-
ponent in equation 3 is aggregate GPR. The second component interacts aggregate
( )
GPR with industry exposure , capturing the idea that some industries may be
Λ k
disproportionately affected by aggregate geopolitical risks. For instance, defense
or petroleum companies may be particularly affected by geopolitical tensions in
the Middle East, while airlines may be highly exposed to the fallout from terrorist
attacks. The third component, Z , is idiosyncratic and isolates fi rm-level geopoliti-
i,t
cal risks that are not reflected at the aggregate and industry levels.
We first describe how we calculate industry exposure . We regress daily port-
Λk
folio returns in the 49 industry groups of Fama and French 1997 on changes in the
( )
daily GPR index:
4 R GPR ,
( ) k,t = αk + βk Δ t + εk ,t

## Page 27
1220 THE AMERICAN ECONOMIC REVIEW APRIL 2022
where R is the annualized daily excess return in industry k over the one month
k ,t
Treasury bill rate and GPR is the change in the daily GPR index. The sample runs
Δ t
from 1985 through 2019. Our idea is that stock returns in sectors with higher expo-
sure drop relatively more than the aggregate market in response to spikes in the GPR
index. By contrast, sectors with lower exposure tend to gain from geopolitical risks
relative to the market. For instance, on September 17, 2001, the day the stock market
reopened after 9 11, the returns in the transportation and precious metals sectors
/
were 13 and 7.4 percent, respectively. This example underscores the importance
− +
of using daily data. Stock prices quickly react to news. Daily data also allow for a
more granular taxonomy of geopolitical risks that, for episodes that do not dominate
the news cycle for a prolonged period, is partly lost by aggregating data to monthly
or quarterly frequencies.
We estimate the coefficients in equation 4 , demean them and change their
βk ( )
sign so that positive values indicate high exposure. Figure A.8 in the online Appendix
plots the average exposure by industry. Precious metals, petroleum, and defense are
among the industries negatively exposed to increases in geopolitical risk. Shipping
and transportation are among the industries with positive exposure. For our empir-
ical application below, the exposure measure is a dummy that equals one for
Λk
industries with a bove-median exposure, and zero otherwise.22
Next, we turn to the measurement of idiosyncratic geopolitical risk Z . A com-
i ,t
pany might face elevated geopolitical risks because it operates in countries whose
events are not reflected in the aggregate and industry measure e.g., an oil company
(
operating in Gabon . Alternatively, a company could have unique and time-varying
)
exposure to aggregate geopolitical events, due to its location, political connections,
trade exposure, or risk-management strategies.
Following Hassan et al. 2019 , we perform text analysis on the transcripts of
( )
quarterly earnings calls of US-listed firms. The sample runs from 2005:I through
2019:IV. We construct fi rm-level geopolitical risk by counting mentions of adverse
geopolitical events and risks in the earnings calls. Specifically, we count the joint
occurrences of “risk” words within ten words of “geopolitical” words, normalizing
the counts by the total number of words in the transcript.23 In online Appendix
Figure A.9, we plot the GPR index alongside the index obtained by aggregating
across firms, each quarter, the transcripts that discuss concerns about geopolitical
risk. The correlation between the two indices is 0.19. The positive correlation, albeit
calculated on a short sample, bolsters our confidence that investors’ and newspapers
concerns about geopolitical events are aligned.
B. Dynamic Effects of Industry-Specific Geopolitical Risk
We quantify the differential effects of geopolitical risk on investment across
industries. Using Compustat data, we measure investment as the ratio of capital
expenditures to previous-period property, plant, and equipment, and denote it by i k .
22 The use of a dummy makes the estimation more robust to the exact quantification of exposure. Results using
the coefficients as a measure of exposure are similar and are shown in the online Appendix Table A.7.
β23
See online Appendix E.3 for details. Examples of geopolitical words include “war,” “mil
(
itary,” “terr
)
or,” “con-
flict,” “coup,” and “embargo.” Examples of risk words include “risk,” “potential,” “danger,” “dispute,” “incident,”
and “attack.”

## Page 28
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1221
We regress fi rm-level investment at various horizons against aggregate GPR inter-
acted with industry exposure. Our baseline strategy follows the local projection
approach developed by Jorda 2005 . We estimate
( )
5 logik logGPR d X ,
( ) i ,t + h = αi ,h + βh ( 픻핂 Δ t ) + h i ,t + εi ,t + h
where h 0 indices current and future quarters. The goal is to estimate, for each
≥
horizon h , the sequence of regression coefficients associated with the interaction
βh
between aggregate geopolitical risk and industry exposure. In the equation above,
denotes firm fixed effects. The term logGPR is the product of the industry
αi 픻핂 Δ t
exposure dummy times log changes in aggregate geopolitical risk. The term X
i ,t
denotes control variables, namely firm-level cash flows, firm-level Tobin’s Q, and
the lagged value of log ik .
i ,t
The top panel of Figure 11 shows the differential response of firm-level invest-
ment to a t wo standard deviation aggregate GPR shock, for a firm belonging to an
industry with high exposure to GPR. In the first year after the shock, an exposed
firm experiences a decline in investment that is about 1 percentage point larger than
its nonexposed counterpart. These estimates indicate that the negative repercussions
of a typical spike in geopolitical risk on the investment rate vary depending on the
industry of operation.
We conclude with a cautionary note on how to interpret our industry regressions.
Our approach can be interpreted through the lens of a two-stage regression. In the
first stage, we extract industry exposure by regressing stock returns on daily geo-
political risk industry-by-industry. In the second stage, we look at how investment
responds to geopolitical risk depending on industry exposure. Accordingly, our sec-
ond regression has the flavor of an instrumental variables regression of industry
investment on industry stock returns where the instruments are industry dummies
interacted with GPR. That said, our regression does not merely confirm that invest-
ment and stock prices are positively correlated, but also shows that movements in
geopolitical risk affect some industries more than others, and that the differential
effect is captured by the differential response of stock prices.24
C. Dynamic Effects of Firm-Specific Geopolitical Risk
To assess the dynamic relationship between investment and geopolitical risk at
the firm level, we estimate
6 logik Z d X
( ) i ,t + h = αi ,h + αk ,t,h + γ h i,t + h i ,t + εi ,t + h .
The goal is to estimate, for each horizon h 0 , the coefficient which mea-
≥ γh
sures the dynamic effect on investment of changes in fi rm-level geopolitical risk.
The regression includes firm fixed effects and sector-by-quarter dummies .
( α i ) ( α k,t )
Firm-control variables X include firm-level cash flows, firm-level Tobin’s Q, and
i,t
log ik .
i ,t
−
1
24 Alfaro, Bloom, and Lin 2018 look at differential firms exposure to energy prices, exchange rates, and eco-
( )
nomic uncertainty shocks and use the differential exposures to draw conclusions about the effects of uncertainty.

## Page 29
1222 THE AMERICAN ECONOMIC REVIEW APRIL 2022
1
0
1
−
2
−
Figure 11. Response of F irm-Level Investment to Geopolitical Risk
Notes: The top panel plots the dynamic response of investment following a two standard deviation increase in
aggregate GPR for a firm in an industry with positive exposure to geopolitical risk. The bottom panel plots the
dynamic response of investment following a two standard deviation increase in firm-level GPR. The shaded areas
denote 90 percent confidence intervals. Standard errors are two-way clustered by firm and quarter-industry.
Mentions of geopolitical risks in the text of the earnings calls are a proxy for
GPR , as the typical earnings call of a firm contains references to idiosyn-
i,t
cratic as well as aggregate and industry-specific geopolitical risks. To isolate the
firm-specific component Z , we absorb the aggregate and industry-specific com-
i,t
ponents by including in equation 6 sector-by-quarter dummies. Our sample runs
( )
from 2005:I through 2019:IV and is dictated by the availability of the earnings
calls data.
The bottom panel of Figure 11 plots the response of fi rm-level investment the
(
sequence of coefficients at different horizons after an increase in fi rm-level GPR
γh )
of two standard deviations. Firms gradually reduce their investment over the two
quarters after the shock, with investment declining more than 1 percent at the trough
and staying below the baseline for up to one year.
D. Summary of F irm-Level Evidence
Table 5 summarizes the analysis, tabulating the investment response to changes
in geopolitical risk at the firm and industry levels. We focus on the response of
investment two quarters ahead, in line with the results from the local projections
that show that changes in geopolitical risk materialize with a delay of one to two
quarters. In columns 1 and 2, investment responds to changes in geopolitical risk
more for industries with a bove-average exposure. In column 3, investment at the
firm level is negatively associated with changes in firm-level geopolitical risk. Of
note, in column 4, the response estimated with our firm-level variable is similar in
sign and magnitude to the response of fi rm-level investment to firm-level political
esnopser
tnecreP
Firm-level investment: response to GPR of exposed industries
0 2 4 6
Quarters
1
0
1
−
2
−
3
−
esnopser
tnecreP
Firm-level investment: response to idiosyncratic GPR
0 2 4 6
Quarters

## Page 30
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1223
Table 5—Geopolitical Risk and Firm-Level Investment
IKt 2 1 2 3 4
( + ) ( ) ( ) ( ) ( )
GPR dummy industry exposure 0.63 0.64
Δ × − −
0.29 0.27
( ) ( )
GPR firm level 0.67
−
0.30
( )
GPR 1.39
Δ −
1.19
( )
Political risk Hassan et al. 2019 0.75
( ) −
0.25
( )
Cash flow 2.72 2.78 2.67 2.48
0.46 0.46 0.38 0.30
( ) ( ) ( ) ( )
Tobin’s Q 8.91 7.93 9.31 9.47
1.68 1.56 0.92 0.90
( ) ( ) ( ) ( )
0.31 0.30 0.24 0.26
IKt 1
( − ) 0.01 0.01 0.01 0.01
( ) ( ) ( ) ( )
Observations 374,727 374,727 95,073 112,161
Firm fixed effects Yes Yes Yes Yes
Time effects No Yes Yes Yes
R2 0.45 0.47 0.59 0.58
Sample 85Q1–19Q4 85Q1–19Q4 05Q1–19Q4 05Q1–19Q4
Notes: Standard errors, in parentheses, are clustered by industry and quarter in columns 1 and 2, by firm and
quarter-industry in columns 3 and 4. The table shows results from regressions of firm-level investment on geopo-
litical risk at the industry or at the firm level. The dependent variable IK is defined as 100 log ik, where ik is the
×
ratio of capital expenditures to previous-period property, plant, and equipment, as defined in the text. All variables
except the dummy exposure variable are standardized.
( )
risk as measured by Hassan et al. 2019 .25 Overall, changes in geopolitical risks are
( )
associated with heterogeneous effects on firm investment, depending on the indus-
try of operation and on fi rm-specific risks. The link between geopolitical risk and
firm-level activity is significant, economically meaningful, and persistent over time.
VI. Conclusions
We propose and implement indicators of geopolitical risk that measure the threat,
realization, and escalation of adverse geopolitical events. A detailed set of validation
exercises confirm that our GPR indices accurately capture the timing and intensity of
adverse geopolitical events, both across countries and over time. Higher geopolitical
risk foreshadows lower investment and is associated with higher disaster probability
and larger downside risks to GDP growth. The adverse consequences of geopolitical
risk are stronger for firms in more exposed industries, and high fi rm-level geopolit-
ical risk is associated with lower firm-level investment.26
We conclude highlighting three areas for future research.
25 The measure by Hassan et al. 2019 is a broader concept of risk at the firm level encompassing concerns for
( )
instance about the government budget, health care, trade, and national security.
26 While we find that higher geopolitical risk is associated with adverse economic outcomes, we caution that our
empirical analysis is limited to analyzing past historical events. Future geopolitical risks could take different forms
and yield different economic effects than in the past.

## Page 31
1224 THE AMERICAN ECONOMIC REVIEW APRIL 2022
First, an implicit hypothesis underlying the construction of our indices is that
newspapers’ attention to geopolitical events is an accurate measure of the per-
ceptions of investors, economic agents, and policymakers. It would be useful in
the future to extend our measurement exercise using additional sources, such as
foreign-language publications, periodical country reports, or the transcripts of par-
liamentary debates.
Second, an important extension would be to investigate the international ramifi-
cations of geopolitical risks. Geopolitical risks can impact the price of risky assets
and the flow of capital across countries. In a similar vein, tensions among countries
can be an important force shaping trade flows and global supply chains through
firms’ actions and government policies.
Finally, in the empirical analysis, we have treated geopolitical risk as a driver of
business fluctuations, highlighting a new force and a new set of shocks that econo-
mists have not traditionally emphasized. That said, an active literature in economics
and political science has worked to better understand the causes of internal con-
flict and interstate warfare see e.g., Blattman and Miguel 2010 and Jackson and
(
Morelli 2011, among others . We hope that our measures can help researchers to
)
better address these questions as well.
REFERENCES
Alfaro, Ivan, Nicholas Bloom, and Xiaoji Lin. 2018. “The Finance Uncertainty Multiplier.” NBER
Working Paper 24571.
Baker, Scott R., Nicholas Bloom, and Steven J. Davis. 2016. “Measuring Economic Policy Uncer-
tainty.” Quarterly Journal of Economics 131 4 : 1593–1636.
( )
Barro, Robert J. 2006. “Rare Disasters and Asset Markets in the Twentieth Century.” Quarterly Jour-
nal of Economics 121 3 : 823–66.
( )
Barro, Robert J., and José F. Ursúa. 2012. “Rare Macroeconomic Disasters.” Annual Review of Eco-
nomics 4 1 : 83–109.
( )
Bazzi, Samuel, and Christopher Blattman. 2014. “Economic Shocks and Conflict: Evidence from
Commodity Prices.” American Economic Journal: Macroeconomics 6 4 : 1–38.
( )
Beaudry, Paul, and Franck Portier. 2006. “Stock Prices, News, and Economic Fluctuations.” American
Economic Review 96 4 : 1293–1307.
( )
Bergeaud, Antonin, Gilbert Cette, and Rémy Lecat. 2016. “Productivity Trends in Advanced Countries
between 1890 and 2012.” Review of Income and Wealth 62 3 : 420–44.
( )
Berger, David, Ian Dew-Becker, and Stefano Giglio. 2019. “Uncertainty Shocks as Second-Moment
News Shocks.” Review of Economic Studies 87 1 : 40–76.
( )
Berkman, Henk, Ben Jacobsen, and John B. Lee. 2011. “Time-Varying Rare Disaster Risk and Stock
Returns.” Journal of Financial Economics 101 2 : 313–32.
( )
Blattman, Christopher, and Edward Miguel. 2010. “Civil War.” Journal of Economic Literature
48 1 : 3–57.
( )
Bloom, Nicholas. 2009. “The Impact of Uncertainty Shocks.” Econometrica 77 3 : 623–85.
( )
Bloom, Nicholas, Max Floetotto, Nir Jaimovich, Itay Saporta-Eksten, and Stephen J. Terry. 2018.
“Really Uncertain Business Cycles.” Econometrica 86 3 : 1031–65.
( )
Caldara, Dario, Cristina Fuentes-Albero, Simon Gilchrist, and Egon Zakrajšek. 2016. “The Macroeco-
nomic Impact of Financial and Uncertainty Shocks.” European Economic Review 88 C : 185–207.
( )
Caldara, Dario, and Matteo Iacoviello. 2022. “Replication Data for: Measuring Geopolitical Risk.”
American Economic Association publisher, Inter-university Consortium for Political and Social
[ ]
Research distributor. https://doi.org/10.3886/E154781V1.
[ ]
Carney, Mark. 2016. “Uncertainty, the Economy and Policy.” Speech, Bank of England, London,
June 30. https://www.bis.org/review/r160704c.pdf.
Dijkink, Gertjan. 2009. “Geopolitics and Religion.” In International Encyclopedia of Human Geogra-
phy, edited by Rob Kitchin and Nigel Thrift, 453–57. Oxford: Elsevier.
Fama, Eugene F., and Kenneth R. French. 1997. “Industry Costs of Equity.” Journal of Financial Eco-
nomics 43 2 : 153–93.
( )

## Page 32
VOL. 112 NO. 4 CALDARA AND IACOVIELLO: MEASURING GEOPOLITICAL RISK 1225
Flint, Colin. 2016. Introduction to Geopolitics. Oxfordshire: Routledge.
Foster, John Bellamy. 2006. “The New Geopolitics of Empire.” Monthly Review 57 8 : 1–18.
( )
Gentzkow, Matthew, Bryan Kelly, and Matt Taddy. 2019. “Text as Data.” Journal of Economic Liter-
ature 57 3 : 535–74.
( )
Glick, Reuven, and Alan M. Taylor. 2010. “Collateral Damage: Trade Disruption and the Economic
Impact of War.” Review of Economics and Statistics 92 1 : 102–27.
( )
Gourio, Francois. 2008. “Disasters and Recoveries.” American Economic Review 98 2 : 68–73.
( )
Hassan, Tarek A., Stephan Hollander, Laurence van Lent, and Ahmed Tahoun. 2019. “Firm-Level
Political Risk: Measurement and Effects.” Quarterly Journal of Economics 134 4 : 2135–2202.
( )
Ilut, Cosmin L., and Martin Schneider. 2014. “Ambiguous Business Cycles.” American Economic
Review 104 8 : 2368–99.
( )
Jackson, Matthew O., and Massimo Morelli. 2011. “The Reasons for Wars: An Updated Survey.” In
The Handbook on the Political Economy of War, edited by Christopher J. Coyne and Rachel L.
Mathers, 34–57. Cheltenham, England: Edward Elgar Publishing Limited.
Jaimovich, Nir, and Sergio Rebelo. 2009. “Can News about the Future Drive the Business Cycle?”
American Economic Review 99 4 : 1097–1118.
( )
Jorda, Oscar. 2005. “Estimation and Inference of Impulse Responses by Local Projections.” American
Economic Review 95 1 : 161–82.
( )
Kozlowski, Julian, Laura Veldkamp, and Venky Venkateswaran. 2018. “The Tail that Keeps the Risk-
less Rate Low.” NBER Working Paper 24362.
Ludvigson, Sydney C., Sai Ma, and Serena Ng. 2021. “Uncertainty and Business Cycles: Exoge-
nous Impulse or Endogenous Response?” American Economic Journal: Macroeconomics 13 4 :
( )
369–410.
Nakamura, Emi, Jón Steinsson, Robert Barro, and José Ursúa. 2013. “Crises and Recoveries in an
Empirical Model of Consumption Disasters.” American Economic Journal: Macroeconomics 5 3 :
( )
35–74.
Pindyck, Robert S., and Neng Wang. 2013. “The Economic and Policy Consequences of Catastro-
phes.” American Economic Journal: Economic Policy 5 4 : 306–39.
( )
Ramey, Valerie A. 2011. “Identifying Government Spending Shocks: It’s All in the Timing.” Quarterly
Journal of Economics 126 1 : 1–50.
( )
Ramey, Valerie A., and Sarah Zubairy. 2018. “Government Spending Multipliers in Good Times and
in Bad: Evidence from US Historical Data.” Journal of Political Economy 126 2 : 850–901.
( )
Rogers, Alisdair, Noel Castree, and Rob Kitchin. 2013. A Dictionary of Human Geography. Oxford:
Oxford University Press.
Rosenthal, Jack. 2004. “The Public Editor; What Belongs on the Front Page of The New York Times.”
New York Times, August 22.
Roser, Max, and Mohamed Nagdy. 2013. “Military Spending.” Our World in Data. https://
ourworldindata.org/military-spending.
Saiz, Albert, and Uri Simonsohn. 2013. “Proxying for Unobservable Variables with Internet Docu-
ment-Frequency.” Journal of the European Economic Association 11 1 : 137–65.
( )
Sherwin, Martin J. 2012. “The Cuban Missile Crisis at 50: In Search of Historical Perspective.” Pro-
logue Magazine 44 3 : 6–16.
( )
Stein, Arthur A., and Bruce Russett. 1980. “Evaluating War: Outcomes and Consequences.” In Hand-
book of Political Conflict: Theory and Research, edited by Ted Robert Gurr, 399–422. New York:
Free Press.
