% Make a suggested move
% Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
% Returns False if this is an invalid move, True if it is valid.
% Edward Stevinson 18/7/16
%%

function [bool, board] = makeMove(board, colour, xstart, ystart)


    % Change so doesn't fail if not given a move!
    [valid, tilesToFlip] = othello_scripts.isValidMove(board, colour, xstart, ystart);

    if (valid == false)
        bool = false;
    else
        board.positions(xstart, ystart) = colour;
        for j = 1:size(tilesToFlip,1)
            x_temp = tilesToFlip(j,1);
            y_temp = tilesToFlip(j,2);
            board.positions(x_temp,y_temp) = colour;
        end
        bool = true;
    end

end