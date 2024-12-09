 The chess project is a web-based chess running on a Flask server and using Python
along with various 3rd party libraries, the most notable being python-chess. The ap
plication provides the user with an online chess interface, and numerous other features
 aimed at both novices and advanced players alike. It allows players to graphically in
put moves using algebraic chess notation; it also provides the ability to connect to
 various engines such as Stockfish or Dev-Zero, amongst others and automatically gen
erate moves. Several sophisticated algorithms are also implemented within the system
 to cater for aspects such as move selection or take care of game context evaluation
 and even simulate players behavior. The core of the architecture design is based on
 the Min-Max algorithm with alpha-beta pruning, this allows the AI to enumerate
 upto all possible moves, however, those moves are evaluated via dynamically assigned
 game state values which are generically based on recursive future states of the game.
 This particular strategy would enable the AI to yield a better result by choosing a
 move where a user’s potential is maximized and the opponent’s potential is mini
mized. Alpha-Beta pruning is used to resolve certain weaknesses not only of standard
 minimax but also to improve its performance by minimizing the number of positions
 searched automatically. In more complex positions the algorithm applies Quiescence
 search and the fourth part of length one in more complicated positions where captures
 or checks occur. This is to prevent the AI from being too trigger happy when the
 context of the evaluation could lead to misunderstanding such as in tactical slogs.
 To further enhance the evaluation, the system is provided with piece-square tables
 which assign values to squares depending on the type of piece occupying them. These
 tables modify the evaluation based upon the location of a specific piece and act as
 a guide to the AI on where to look for advantageous positions and where to decide
 to engage. Apart from these core algorithms, the application can communicate with
 UCI (Universal Chess Interface) engines that possess advanced evaluation techniques
 and searching methods for computing moves, for example, Stockfish. Such engines
 increase intelligence of the game by employing deep searching algorithms and complex
 evaluation functions. Finally, the application is enhanced with a text to speech en
gine, which provides audio information about some in-game events like a game status
 as well as announcements of moves made, making the interaction better. These algorithms are essential in developing the chess-playing AI of the
 application, allowing it to take reasonably thoughtful and strategic moves all while
 being entertaining and responsive in interaction with players.
