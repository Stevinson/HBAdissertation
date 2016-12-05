% Function that returns true if the proposed move is valid
% Also returns a list of spaces that would become the player's if they made a move here.
% Edward Stevinson 19/7/16
%%

function [valid_bool, tilesToFlip] = isValidMove(board, tile_colour, xstart, ystart)

    import othello_scripts.*
    
    % Returns False if the player's move on space xstart, ystart is invalid.
    % If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if (board.positions(xstart, ystart) ~= 0) 
        valid_bool = false;
        tilesToFlip = [];
        return 
    end

    if tile_colour == 1
        otherTile = 2;
    else
        otherTile = 1;
    end
    
    directions = [0, 1; 1, 1; 1, 0; 1, -1; 0, -1; -1, -1; -1, 0; -1, 1];
    tilesToFlip = [];
    
    for i = 1:8
        
        x = xstart; y = ystart;
        % first step in the direction
        x = x + directions(i,1); 
        y = y + directions(i,2);
        
        if isOnBoard(x,y) && (board.positions(x,y) == otherTile) 
            
            % There is a piece belonging to the other player next to our piece.
            x = x + directions(i,1); 
            y = y + directions(i,2);
            
            % Square looking at is on board
            if isOnBoard(x, y)
                while board.positions(x,y) == otherTile
                    % further step in the direction
                    x = x + directions(i,1); 
                    y = y + directions(i,2);
                    if ~(isOnBoard(x, y)) 
                         break
                    end
                end
            
                % To flip pieces over one must have same colour at the other side.
                % Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                if isOnBoard(x,y) && (board.positions(x,y) == tile_colour)  
                    while (true)
                        x = x - directions(i,1); 
                        y = y - directions(i,2);
                        if (x == xstart) && (y == ystart)
                             break
                        end
                        tilesToFlip = [tilesToFlip; [x, y]];
                    end    
                end
            end
        end
    end

    % If no tiles were flipped, this is not a valid move.
    if (size(tilesToFlip,1)) == 0 
        valid_bool = false;
        return
    else 
        % Otherwise it is a valid move
        valid_bool = true;
    end
    
end

    

