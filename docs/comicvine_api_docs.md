
Responses
Resources
character
characters
chat
chats
concept
concepts
episode
episodes
issue
issues
location
locations
movie
movies
object
objects
origin
origins
person
people
power
powers
promo
promos
publisher
publishers
series
series_list
search
story_arc
story_arcs
team
teams
types
video
videos
video_type
video_types
video_category
video_categories
volume
volumes

Responses
status_code	An integer indicating the result of the request. Acceptable values are:
1:OK
100:Invalid API Key
101:Object Not Found
102:Error in URL Format
103:'jsonp' format requires a 'json_callback' argument
104:Filter Error
105:Subscriber only video is for subscribers only
error	A text string representing the status_code
number_of_total_results	The number of total results matching the filter conditions specified
number_of_page_results	The number of results on this page
limit	The value of the limit filter specified, or 100 if not specified
offset	The value of the offset filter specified, or 0 if not specified
results	Zero or more items that match the filters specified

Resources
character
URL: /character
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the character is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the character detail resource.
birth	A date, if one exists, that the character was born on. Not an origin date.
character_enemies	List of characters that are enemies with this character.
character_friends	List of characters that are friends with this character.
count_of_issue_appearances	Number of issues this character appears in.
creators	List of the real life people who created this character.
date_added	Date the character was added to Comic Vine.
date_last_updated	Date the character was last updated on Comic Vine.
deck	Brief summary of the character.
description	Description of the character.
first_appeared_in_issue	Issue where the character made its first appearance.
gender	Gender of the character. Available options are: Male, Female, Other
id	Unique ID of the character.
image	Main image of the character.
issue_credits	List of issues this character appears in.
issues_died_in	List of issues this character died in.
movies	Movies the character was in.
name	Name of the character.
origin	The origin of the character. Human, Alien, Robot ...etc
powers	List of super powers a character has.
publisher	The primary publisher a character is attached to.
real_name	Real name of the character.
site_detail_url	URL pointing to the character on Giant Bomb.
story_arc_credits	List of story arcs this character appears in.
team_enemies	List of teams that are enemies of this character.
team_friends	List of teams that are friends with this character.
teams	List of teams this character is a member of.
volume_credits	List of comic volumes this character appears in.

characters
URL: /characters
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the character is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the character detail resource.		
birth	A date, if one exists, that the character was born on. Not an origin date.		
count_of_issue_appearances	Number of issues this character appears in.		
date_added	Date the character was added to Comic Vine.		
date_last_updated	Date the character was last updated on Comic Vine.		
deck	Brief summary of the character.		
description	Description of the character.		
first_appeared_in_issue	Issue where the character made its first appearance.		
gender	Gender of the character. Available options are: Male, Female, Other		
id	Unique ID of the character.		
image	Main image of the character.		
name	Name of the character.		
origin	The origin of the character. Human, Alien, Robot ...etc		
publisher	The primary publisher a character is attached to.		
real_name	Real name of the character.		
site_detail_url	URL pointing to the character on Giant Bomb.		

chat
URL: /chat
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
api_detail_url	URL pointing to the chat detail resource.
channel_name	Name of the video streaming channel associated with the chat.
deck	Brief summary of the chat.
image	Main image of the chat.
password	chat password.
site_detail_url	URL pointing to the chat on Giant Bomb.
title	Title of the chat.

chats
URL: /chats
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
api_detail_url	URL pointing to the chat detail resource.
channel_name	Name of the video streaming channel associated with the chat.
deck	Brief summary of the chat.
image	Main image of the chat.
password	chat password.
site_detail_url	URL pointing to the chat on Giant Bomb.
title	Title of the chat.

concept
URL: /concept
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the concept is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the concept detail resource.
count_of_issue_appearances	Number of issues this concept appears in.
date_added	Date the concept was added to Comic Vine.
date_last_updated	Date the concept was last updated on Comic Vine.
deck	Brief summary of the concept.
description	Description of the concept.
first_appeared_in_issue	Issue where the concept made its first appearance.
id	Unique ID of the concept.
image	Main image of the concept.
issue_credits	List of issues this concept appears in.
movies	Movies the concept was in.
name	Name of the concept.
site_detail_url	URL pointing to the concept on Giant Bomb.
start_year	The first year this concept appeared in comics.
volume_credits	List of comic volumes this concept appears in.

concepts
URL: /concepts
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the concept is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the concept detail resource.		
count_of_issue_appearances	Number of issues this concept appears in.		
date_added	Date the concept was added to Comic Vine.		
date_last_updated	Date the concept was last updated on Comic Vine.		
deck	Brief summary of the concept.		
description	Description of the concept.		
first_appeared_in_issue	Issue where the concept made its first appearance.		
id	Unique ID of the concept.		
image	Main image of the concept.		
name	Name of the concept.		
site_detail_url	URL pointing to the concept on Giant Bomb.		
start_year	The first year this concept appeared in comics.		

episode
URL: /episode
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the episode is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the episode detail resource.
character_credits	A list of characters that appear in this episode.
characters_died_in	A list of characters that died in this episode.
concept_credits	A list of concepts that appear in this episode.
air_date	The air date of the episode.
date_added	Date the episode was added to Comic Vine.
date_last_updated	Date the episode was last updated on Comic Vine.
deck	Brief summary of the episode.
description	Description of the episode.
first_appearance_characters	A list of characters in which this episode is the first appearance of the character.
first_appearance_concepts	A list of concepts in which this episode is the first appearance of the concept.
first_appearance_locations	A list of locations in which this episode is the first appearance of the location.
first_appearance_objects	A list of objects in which this episode is the first appearance of the object.
first_appearance_storyarcs	A list of storyarcs in which this episode is the first appearance of the story arc.
first_appearance_teams	A list of teams in which this episode is the first appearance of the team.
has_staff_review	
id	Unique ID of the episode.
image	Main image of the episode.
episode_number	The number assigned to the episode within a series.
location_credits	List of locations that appeared in this episode.
name	Name of the episode.
object_credits	List of objects that appeared in this episode.
person_credits	List of people that worked on this episode.
site_detail_url	URL pointing to the episode on Giant Bomb.
story_arc_credits	List of story arcs this episode appears in.
team_credits	List of teams that appear in this episode.
series	The series the episode belongs to.

episodes
URL: /episodes
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the episode is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the episode detail resource.		
air_date	The air date of the episode.		
date_added	Date the episode was added to Comic Vine.		
date_last_updated	Date the episode was last updated on Comic Vine.		
deck	Brief summary of the episode.		
description	Description of the episode.		
has_staff_review			
id	Unique ID of the episode.		
image	Main image of the episode.		
issue_number	The number assigned to the episode within the volume set.		
name	Name of the episode.		
site_detail_url	URL pointing to the episode on Giant Bomb.		
series	The series the episode belongs to.		

issue
URL: /issue
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the issue is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the issue detail resource.
character_credits	A list of characters that appear in this issue.
characters_died_in	A list of characters that died in this issue.
concept_credits	A list of concepts that appear in this issue.
cover_date	The publish date printed on the cover of an issue.
date_added	Date the issue was added to Comic Vine.
date_last_updated	Date the issue was last updated on Comic Vine.
deck	Brief summary of the issue.
description	Description of the issue.
disbanded_teams	A list of teams that disbanded in this issue.
first_appearance_characters	A list of characters in which this issue is the first appearance of the character.
first_appearance_concepts	A list of concepts in which this issue is the first appearance of the concept.
first_appearance_locations	A list of locations in which this issue is the first appearance of the location.
first_appearance_objects	A list of objects in which this issue is the first appearance of the object.
first_appearance_storyarcs	A list of storyarcs in which this issue is the first appearance of the story arc.
first_appearance_teams	A list of teams in which this issue is the first appearance of the team.
has_staff_review	
id	Unique ID of the issue.
image	Main image of the issue.
issue_number	The number assigned to the issue within the volume set.
location_credits	List of locations that appeared in this issue.
name	Name of the issue.
object_credits	List of objects that appeared in this issue.
person_credits	List of people that worked on this issue.
site_detail_url	URL pointing to the issue on Giant Bomb.
store_date	The date the issue was first sold in stores.
story_arc_credits	List of story arcs this issue appears in.
team_credits	List of teams that appear in this issue.
teams_disbanded_in	List of teams that disbanded in this issue.
volume	The volume this issue is a part of.

issues
URL: /issues
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the issue is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the issue detail resource.		
cover_date	The publish date printed on the cover of an issue.		
date_added	Date the issue was added to Comic Vine.		
date_last_updated	Date the issue was last updated on Comic Vine.		
deck	Brief summary of the issue.		
description	Description of the issue.		
has_staff_review			
id	Unique ID of the issue.		
image	Main image of the issue.		
issue_number	The number assigned to the issue within the volume set.		
name	Name of the issue.		
site_detail_url	URL pointing to the issue on Giant Bomb.		
store_date	The date the issue was first sold in stores.		
volume	The volume this issue is a part of.		

location
URL: /location
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the location is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the location detail resource.
count_of_issue_appearances	Number of issues this location appears in.
date_added	Date the location was added to Comic Vine.
date_last_updated	Date the location was last updated on Comic Vine.
deck	Brief summary of the location.
description	Description of the location.
first_appeared_in_issue	Issue where the location made its first appearance.
id	Unique ID of the location.
image	Main image of the location.
issue_credits	List of issues this location appears in.
movies	Movies the location was in.
name	Name of the location.
site_detail_url	URL pointing to the location on Giant Bomb.
start_year	The first year this location appeared in comics.
story_arc_credits	List of story arcs this location appears in.
volume_credits	List of comic volumes this location appears in.

locations
URL: /locations
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the location is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the location detail resource.		
count_of_issue_appearances	Number of issues this location appears in.		
date_added	Date the location was added to Comic Vine.		
date_last_updated	Date the location was last updated on Comic Vine.		
deck	Brief summary of the location.		
description	Description of the location.		
first_appeared_in_issue	Issue where the location made its first appearance.		
id	Unique ID of the location.		
image	Main image of the location.		
name	Name of the location.		
site_detail_url	URL pointing to the location on Giant Bomb.		
start_year	The first year this location appeared in comics.		

movie
URL: /movie
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
api_detail_url	URL pointing to the movie detail resource.
box_office_revenue	The total revenue made in the box offices for this movie.
budget	The cost of making this movie.
characters	Characters related to the movie.
concepts	Concepts related to the movie.
date_added	Date the movie was added to Comic Vine.
date_last_updated	Date the movie was last updated on Comic Vine.
deck	Brief summary of the movie.
description	Description of the movie.
distributor	
has_staff_review	
id	Unique ID of the movie.
image	Main image of the movie.
locations	Locations related to the movie.
name	Name of the movie.
producers	The producers of this movie.
rating	The rating of this movie.
release_date	Date of the movie.
runtime	The length of this movie.
site_detail_url	URL pointing to the movie on Giant Bomb.
studios	
teams	List of teams this movie is a member of.
things	List of things found in this movie.
total_revenue	Total revenue generated by this movie.
writers	Writers for this movie.

movies
URL: /movies
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
api_detail_url	URL pointing to the movie detail resource.		
box_office_revenue	The total revenue made in the box offices for this movie.		
budget	The cost of making this movie.		
date_added	Date the movie was added to Comic Vine.		
date_last_updated	Date the movie was last updated on Comic Vine.		
deck	Brief summary of the movie.		
description	Description of the movie.		
distributor			
has_staff_review			
id	Unique ID of the movie.		
image	Main image of the movie.		
name	Name of the movie.		
producers	The producers of this movie.		
rating	The rating of this movie.		
release_date	Date of the movie.		
runtime	The length of this movie.		
site_detail_url	URL pointing to the movie on Giant Bomb.		
studios			
total_revenue	Total revenue generated by this movie.		
writers	Writers for this movie.		

object
URL: /object
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the object is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the object detail resource.
count_of_issue_appearances	Number of issues this object appears in.
date_added	Date the object was added to Comic Vine.
date_last_updated	Date the object was last updated on Comic Vine.
deck	Brief summary of the object.
description	Description of the object.
first_appeared_in_issue	Issue where the object made its first appearance.
id	Unique ID of the object.
image	Main image of the object.
issue_credits	List of issues this object appears in.
movies	Movies the object was in.
name	Name of the object.
site_detail_url	URL pointing to the object on Giant Bomb.
start_year	The first year this object appeared in comics.
story_arc_credits	List of story arcs this object appears in.
volume_credits	List of comic volumes this object appears in.

objects
URL: /objects
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the object is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the object detail resource.		
count_of_issue_appearances	Number of issues this object appears in.		
date_added	Date the object was added to Comic Vine.		
date_last_updated	Date the object was last updated on Comic Vine.		
deck	Brief summary of the object.		
description	Description of the object.		
first_appeared_in_issue	Issue where the object made its first appearance.		
id	Unique ID of the object.		
image	Main image of the object.		
name	Name of the object.		
site_detail_url	URL pointing to the object on Giant Bomb.		
start_year	The first year this object appeared in comics.		

origin
URL: /origin
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
api_detail_url	URL pointing to the origin detail resource.
character_set	
id	Unique ID of the origin.
name	Name of the origin.
profiles	
site_detail_url	URL pointing to the origin on Giant Bomb.

origins
URL: /origins
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
api_detail_url	URL pointing to the origin detail resource.		
id	Unique ID of the origin.		
name	Name of the origin.		
site_detail_url	URL pointing to the origin on Giant Bomb.		

person
URL: /person
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the person is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the person detail resource.
birth	A date, if one exists, that the person was born on. Not an origin date.
count_of_issue_appearances	Number of issues this person appears in.
country	Country the person resides in.
created_characters	Comic characters this person created.
date_added	Date the person was added to Comic Vine.
date_last_updated	Date the person was last updated on Comic Vine.
death	Date this person died on.
deck	Brief summary of the person.
description	Description of the person.
email	The email of this person.
gender	Gender of the person. Available options are: Male, Female, Other
hometown	City or town the person resides in.
id	Unique ID of the person.
image	Main image of the person.
issue_credits	List of issues this person appears in.
name	Name of the person.
site_detail_url	URL pointing to the person on Giant Bomb.
story_arc_credits	List of story arcs this person appears in.
volume_credits	List of comic volumes this person appears in.
website	URL to the person website.

people
URL: /people
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the person is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the person detail resource.		
birth	A date, if one exists, that the person was born on. Not an origin date.		
count_of_issue_appearances	Number of issues this person appears in.		
country	Country the person resides in.		
date_added	Date the person was added to Comic Vine.		
date_last_updated	Date the person was last updated on Comic Vine.		
death	Date this person died on.		
deck	Brief summary of the person.		
description	Description of the person.		
email	The email of this person.		
gender	Gender of the person. Available options are: Male, Female, Other		
hometown	City or town the person resides in.		
id	Unique ID of the person.		
image	Main image of the person.		
name	Name of the person.		
site_detail_url	URL pointing to the person on Giant Bomb.		
website	URL to the person website.		

power
URL: /power
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the power is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the power detail resource.
characters	Characters related to the power.
date_added	Date the power was added to Comic Vine.
date_last_updated	Date the power was last updated on Comic Vine.
description	Description of the power.
id	Unique ID of the power.
name	Name of the power.
site_detail_url	URL pointing to the power on Giant Bomb.

powers
URL: /powers
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the power is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the power detail resource.		
date_added	Date the power was added to Comic Vine.		
date_last_updated	Date the power was last updated on Comic Vine.		
description	Description of the power.		
id	Unique ID of the power.		
name	Name of the power.		
site_detail_url	URL pointing to the power on Giant Bomb.		

promo
URL: /promo
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
api_detail_url	URL pointing to the promo detail resource.
date_added	Date the promo was added to Comic Vine.
deck	Brief summary of the promo.
id	Unique ID of the promo.
image	Main image of the promo.
link	The link that promo points to.
name	Name of the promo.
resource_type	The type of resource the promo is pointing towards.
user	Author of the promo.

promos
URL: /promos
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
api_detail_url	URL pointing to the promo detail resource.		
date_added	Date the promo was added to Comic Vine.		
deck	Brief summary of the promo.		
id	Unique ID of the promo.		
image	Main image of the promo.		
link	The link that promo points to.		
name	Name of the promo.		
resource_type	The type of resource the promo is pointing towards.		
user	Author of the promo.		

publisher
URL: /publisher
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the publisher is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the publisher detail resource.
characters	Characters related to the publisher.
date_added	Date the publisher was added to Comic Vine.
date_last_updated	Date the publisher was last updated on Comic Vine.
deck	Brief summary of the publisher.
description	Description of the publisher.
id	Unique ID of the publisher.
image	Main image of the publisher.
location_address	Street address of the publisher.
location_city	City the publisher resides in.
location_state	State the publisher resides in.
name	Name of the publisher.
site_detail_url	URL pointing to the publisher on Giant Bomb.
story_arcs	List of story arcs tied to this publisher.
teams	List of teams this publisher is a member of.
volumes	List of volumes this publisher has put out.

publishers
URL: /publishers
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the publisher is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the publisher detail resource.		
date_added	Date the publisher was added to Comic Vine.		
date_last_updated	Date the publisher was last updated on Comic Vine.		
deck	Brief summary of the publisher.		
description	Description of the publisher.		
id	Unique ID of the publisher.		
image	Main image of the publisher.		
location_address	Street address of the publisher.		
location_city	City the publisher resides in.		
location_state	State the publisher resides in.		
name	Name of the publisher.		
site_detail_url	URL pointing to the publisher on Giant Bomb.		

series
URL: /series
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the series is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the series detail resource.
character_credits	A list of characters that appear in this series.
count_of_episodes	Number of episodes included in this series.
date_added	Date the series was added to Comic Vine.
date_last_updated	Date the series was last updated on Comic Vine.
deck	Brief summary of the series.
description	Description of the series.
first_episode	The first episode in this series.
id	Unique ID of the series.
image	Main image of the series.
last_episode	The last episode in this series.
location_credits	List of locations that appeared in this series.
name	Name of the series.
publisher	The primary publisher a series is attached to.
site_detail_url	URL pointing to the series on Giant Bomb.
start_year	The first year this series appeared in comics.

series_list
URL: /series_list
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the series_list is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the series_list detail resource.		
count_of_episodes	Number of episodes included in this series_list.		
date_added	Date the series_list was added to Comic Vine.		
date_last_updated	Date the series_list was last updated on Comic Vine.		
deck	Brief summary of the series_list.		
description	Description of the series_list.		
first_episode	The first episode in this series_list.		
id	Unique ID of the series_list.		
image	Main image of the series_list.		
last_episode	The last episode in this series_list.		
name	Name of the series_list.		
publisher	The primary publisher a series_list is attached to.		
site_detail_url	URL pointing to the series_list on Giant Bomb.		
start_year	The first year this series_list appeared in comics.		

search
URL: /search
Filters
format	The data format of the response takes either xml, json, or jsonp.
api_key	Your API Key
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 10 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
query	The search string.
resources	List of resources to filter results. This filter can accept multiple arguments, each delimited with a ",". Available options are:
character
concept
origin
object
location
issue
story_arc
volume
publisher
person
team
video
subscriber_only	NEED DESCRIPTION
Fields
resource_type	The type of resource the result is mapped to. Available options are:
character
concept
origin
object
location
issue
story_arc
volume
publisher
person
team
video

story_arc
URL: /story_arc
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the story_arc is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the story_arc detail resource.
count_of_issue_appearances	Number of issues this story_arc appears in.
date_added	Date the story_arc was added to Comic Vine.
date_last_updated	Date the story_arc was last updated on Comic Vine.
deck	Brief summary of the story_arc.
description	Description of the story_arc.
first_appeared_in_issue	Issue where the story_arc made its first appearance.
id	Unique ID of the story_arc.
image	Main image of the story_arc.
issues	List of issues included in this story_arc.
movies	Movies the story_arc was in.
name	Name of the story_arc.
publisher	The primary publisher a story_arc is attached to.
site_detail_url	URL pointing to the story_arc on Giant Bomb.

story_arcs
URL: /story_arcs
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the story_arc is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the story_arc detail resource.		
count_of_issue_appearances	Number of issues this story_arc appears in.		
date_added	Date the story_arc was added to Comic Vine.		
date_last_updated	Date the story_arc was last updated on Comic Vine.		
deck	Brief summary of the story_arc.		
description	Description of the story_arc.		
first_appeared_in_issue	Issue where the story_arc made its first appearance.		
id	Unique ID of the story_arc.		
image	Main image of the story_arc.		
name	Name of the story_arc.		
publisher	The primary publisher a story_arc is attached to.		
site_detail_url	URL pointing to the story_arc on Giant Bomb.		

team
URL: /team
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the team is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the team detail resource.
character_enemies	List of characters that are enemies with this team.
character_friends	List of characters that are friends with this team.
characters	Characters related to the team.
count_of_issue_appearances	Number of issues this team appears in.
count_of_team_members	Number of team members in this team.
date_added	Date the team was added to Comic Vine.
date_last_updated	Date the team was last updated on Comic Vine.
deck	Brief summary of the team.
description	Description of the team.
disbanded_in_issues	List of issues this team disbanded in.
first_appeared_in_issue	Issue where the team made its first appearance.
id	Unique ID of the team.
image	Main image of the team.
issue_credits	List of issues this team appears in.
issues_disbanded_in	List of issues this team disbanded in.
movies	Movies the team was in.
name	Name of the team.
publisher	The primary publisher a team is attached to.
site_detail_url	URL pointing to the team on Giant Bomb.
story_arc_credits	List of story arcs this team appears in.
volume_credits	List of comic volumes this team appears in.

teams
URL: /teams
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the team is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the team detail resource.		
count_of_issue_appearances	Number of issues this team appears in.		
count_of_team_members	Number of team members in this team.		
date_added	Date the team was added to Comic Vine.		
date_last_updated	Date the team was last updated on Comic Vine.		
deck	Brief summary of the team.		
description	Description of the team.		
first_appeared_in_issue	Issue where the team made its first appearance.		
id	Unique ID of the team.		
image	Main image of the team.		
name	Name of the team.		
publisher	The primary publisher a team is attached to.		
site_detail_url	URL pointing to the team on Giant Bomb.		

types
URL: /types
Filters
format	The data format of the response takes either xml, json, or jsonp.
Fields
detail_resource_name	The name of the type's detail resource.
id	Unique ID of the type.
list_resource_name	The name of the type's list resource.

video
URL: /video
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
api_detail_url	URL pointing to the video detail resource.
deck	Brief summary of the video.
hd_url	URL to the HD version of the video.
high_url	URL to the High Res version of the video.
id	Unique ID of the video.
image	Main image of the video.
length_seconds	Length (in seconds) of the video.
low_url	URL to the Low Res version of the video.
name	Name of the video.
publish_date	Date the video was published on Comic Vine.
site_detail_url	URL pointing to the video on Giant Bomb.
url	The video's filename.
user	Author of the video.

videos
URL: /videos
Filters
format	The data format of the response takes either xml, json, or jsonp.
api_key	Your API Key
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
subscriber_only	NEED DESCRIPTION
video_type	Filters results by video_type. The value passed to this filter should be the ID of the video_type to filter results by.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
api_detail_url	URL pointing to the video detail resource.		
deck	Brief summary of the video.		
hd_url	URL to the HD version of the video.		
high_url	URL to the High Res version of the video.		
id	Unique ID of the video.		
image	Main image of the video.		
length_seconds	Length (in seconds) of the video.		
low_url	URL to the Low Res version of the video.		
name	Name of the video.		
publish_date	Date the video was published on Comic Vine.		
site_detail_url	URL pointing to the video on Giant Bomb.		
url	The video's filename.		
user	Author of the video.		

video_type
URL: /video_type
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
api_detail_url	URL pointing to the video_type detail resource.
deck	Brief summary of the video_type.
id	Unique ID of the video_type.
name	Name of the video_type.
site_detail_url	URL pointing to the video_type on Giant Bomb.

video_types
URL: /video_types
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
Fields
api_detail_url	URL pointing to the video_type detail resource.
deck	Brief summary of the video_type.
id	Unique ID of the video_type.
name	Name of the video_type.
site_detail_url	URL pointing to the video_type on Giant Bomb.

video_category
URL: /video_category
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
api_detail_url	URL pointing to the video_category detail resource.
deck	Brief summary of the video_category.
id	Unique ID of the video_category.
name	Name of the video_category.
site_detail_url	URL pointing to the video_category on Giant Bomb.

video_categories
URL: /video_categories
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
Fields
api_detail_url	URL pointing to the video_category detail resource.
deck	Brief summary of the video_category.
id	Unique ID of the video_category.
name	Name of the video_category.
site_detail_url	URL pointing to the video_category on Giant Bomb.

volume
URL: /volume
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
Fields
aliases	List of aliases the volume is known by. A \n (newline) seperates each alias.
api_detail_url	URL pointing to the volume detail resource.
character_credits	A list of characters that appear in this volume.
concept_credits	A list of concepts that appear in this volume.
count_of_issues	Number of issues included in this volume.
date_added	Date the volume was added to Comic Vine.
date_last_updated	Date the volume was last updated on Comic Vine.
deck	Brief summary of the volume.
description	Description of the volume.
first_issue	The first issue in this volume.
id	Unique ID of the volume.
image	Main image of the volume.
last_issue	The last issue in this volume.
location_credits	List of locations that appeared in this volume.
name	Name of the volume.
object_credits	List of objects that appeared in this volume.
person_credits	List of people that worked on this volume.
publisher	The primary publisher a volume is attached to.
site_detail_url	URL pointing to the volume on Giant Bomb.
start_year	The first year this volume appeared in comics.
team_credits	List of teams that appear in this volume.

volumes
URL: /volumes
Filters
format	The data format of the response takes either xml, json, or jsonp.
field_list	List of field names to include in the response. Use this if you want to reduce the size of the response payload. This filter can accept multiple arguments, each delimited with a ","
limit	The number of results to display per page. This value defaults to 100 and can not exceed this number.
offset	Return results starting with the object at the offset specified.
sort	The result set can be sorted by the marked fields in the Fields section below. Format: &sort=field:direction where direction is either asc or desc.
filter	The result can be filtered by the marked fields in the Fields section below.

Single filter: &filter=field:value
Multiple filters: &filter=field:value,field:value
Date filters: &filter=field:start value|end value (using datetime format)
Fields	Sort	Filter
aliases	List of aliases the volume is known by. A \n (newline) seperates each alias.		
api_detail_url	URL pointing to the volume detail resource.		
count_of_issues	Number of issues included in this volume.		
date_added	Date the volume was added to Comic Vine.		
date_last_updated	Date the volume was last updated on Comic Vine.		
deck	Brief summary of the volume.		
description	Description of the volume.		
first_issue	The first issue in this volume.		
id	Unique ID of the volume.		
image	Main image of the volume.		
last_issue	The last issue in this volume.		
name	Name of the volume.		
publisher	The primary publisher a volume is attached to.		
site_detail_url	URL pointing to the volume on Giant Bomb.		
start_year	The first year this volume appeared in comics.		
