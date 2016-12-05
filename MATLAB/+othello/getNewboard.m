% Othello MATLAB game
% Edward Stevinson 15/7/16
% Function that draws the boards and the initial pieces on it
%%

function board = getNewboard()

    % Blank array for new board
    board.positions = zeros(8);
    % Set initial black pieces
    board.positions(4,4) = 2; board.positions(5,5) = 2;
    % Set initial white pieces
    board.positions(5,4) = 1; board.positions(4,5) = 1;

end