# BirdStack

Welcome to Birdstack! An all new stacking game! The objective of the game is to make the tallest tower of birds as possible! Each time you successfully stack a layer of birds, the score goes up by one. What does it mean to successfully stack a layer of birds? It means to stop the moving stack of birds, so that some part of the moving stack falls between boundaries of the previous layer in the tower, like so:

Stop the game at any time with the pause button or restart button in the top right corner and the game ends when no part of the moving layer birds is stacked on the original tower.

There are different types of birds that can be stacked, some with positive, some negative, and some purely aesthetic effects. But no matter the effect, the entire bird must be stacked on the tower for the effect to take place.
Now let's meet the birds!

This is *normal birdie*:
![normal birdie](https://user-images.githubusercontent.com/55931451/71562592-2a54f480-2a37-11ea-88f5-f2a913a771cd.png)
This one is always a friend and will make up the majority of the tower. There are no effects that come with this birdie.

This is *invincible birdie*, a positive effect birdie:
![invincible birdie](https://user-images.githubusercontent.com/55931451/71562598-3e98f180-2a37-11ea-999f-2ecec2936d40.png)
Stacking invincible birdie will cause the next layer of moving birdies to span the entire screen. There is no way to end the game with a layer of moving birds that span the entire screen, and so this birdie essentially gives a free point. 

This is *tree birdie*, a positive effect birdie:
![tree birdie](https://user-images.githubusercontent.com/55931451/71562603-49ec1d00-2a37-11ea-8528-d06ff8141d9d.png)
Tree birdie carries a branch with it at all times. When stacked, tree birdie will extend its branch and extend the previous layer of the tower by a birdie-length, extending the platform on which to stack future birdies.

This is *bear birdie*, a negative effect birdie:
![bear birdie](https://user-images.githubusercontent.com/55931451/71562596-3476f300-2a37-11ea-8be1-38275fc4af16.png)
Bear birdie carries a little bear on its head. When stacked, the bear on bear birdie's head will eat an adjacent birdie and, as opposed to tree birdie, shrink the previous layer of the tower by a birdie-length, making it harder to stack future birdies.

This is *squiddy birdie*, a negative effect birdie:
![squid birdie](https://user-images.githubusercontent.com/55931451/71562604-52dcee80-2a37-11ea-9879-0a17de82667f.png)
Squiddy birdie carries a little squid on its head. When stacked, the squid on squiddy birdie's head will squirt squid ink all over the screen, and obstruct vision for two turns.

We made this game with PyGame and used PyMonk to simulate physics within the game. 


