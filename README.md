# distancebot

Discord bot meant to simplify or automate some things I had to do as a Discord admin.
Hosted on Heroku.
Commands :

!tg [username] [time] : Mutes someone for [time] seconds (max 15). Also makes the bot broadcast a TTS message about muting the person.

!lg-send [message] : Sends a message to every user on the sendlist*.

!update : Updates the sendlist*.

!moveall [channel] : Moves every Member in the command caller's Voice Channel to the selected [channel].

!clearplays : Clears messages related to the Rythm bot in the Text Channel where it is called.

* What is the sendlist ? 
Sometimes, we like playing on Wolfy.fr with friends. This game is most fun when 10+ people play it, and it was sometimes hard to find people willing to play. When asked about it, the same people told us they wanted to play but had no way to know when games were going to happen.
That's what the sendlist is about : people subscribe by putting a Reaction on a specific message. The subscribed users are then stored on Firebase.
Everytime a message is broadcast to the subscribed users, we update the local list using the Firebase DB before sending the message.
We are now able to broadcast a message such as "Game tonight at 10PM" to every person that plays with us, and only if they want to receive it.
