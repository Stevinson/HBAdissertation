% Given the board state, what are the valid possile moves?
% Edward Stevinson 15/7/16
%%

function validMoves = getValidMoves(board, colour)

import othello_scripts.*

    validMoves = [];

    for x = 1:8
        for y = 1:8
            [valid, ~ ] = isValidMove(board, colour, x, y);
            if ( valid ~= false)
                validMoves = [validMoves; [x,y] ];
            end
        end
    end
    
end