# Adding new emojis.
 if you open the json file you will see the structure of json as:

 {
     "emoji name":"<:emojiname:emoji's id>"
 }
 where "emoji name" is custom emoji name by which bot will identify the emojis.
 and "<:emojiname:emoji's id>" is how emojis are stored in discord's database and are rendered in discord


# How to get "<:emojiname:emoji's id>"
In desktop version of discord. Type any emoji but before sending them put "\" before its name. After sending this you will recieve something like "<:emojiname:emoji's id>" just copy paste it in json file as a value and key can be any emoji name you want.

# Please do not use same key twice as duplicate entries aren't allowed in json files.

# Please change the emoji names before merging this pr as the names are very unprofessional.