%%
% Template for non-HBA agents
% Edward Stevinson 17/7/16
%  
%%

function f = H1_maximum_disk()

    %import othello.scripts.*
    f = @heuristic;

    function [bestMove, possibleMoves, W] = heuristic(i,~,board,~,W,~)
    
        %if (board.turn==1)    
            import othello_scripts.*

            % Initialise
            possibleMoves = [];
            bestMoves = [99, 99]; % Initialise to 99 for error checking
            changed = false;

            % Get possible moves 
            possibleMoves = othello_scripts.getValidMoves(board, i);

            % Go through all the possible moves and remember the best scoring move
            bestScore = -1;
            for j = 1:size(possibleMoves,1)
                dupeBoard.positions = board.positions;
                x_temp = possibleMoves(j,1); y_temp = possibleMoves(j,2);
                [~, dupeBoard] = makeMove(dupeBoard, i, x_temp, y_temp);
                score = getScore(dupeBoard);
                % Dosnt turn over the tile with the most !!!!
                if (score(i) > bestScore) % If a new best move found
                    bestMoves = [x_temp, y_temp];
                    bestScore = score(i);
                    changed = true;
                elseif (score(i) >= bestScore) % If a move that is equally as good as a previous best move is found
                    bestMoves = [bestMoves; x_temp, y_temp];
                end
            end
            % If there is more than one best move, randomly select a move
            num = size(bestMoves,1);
            if (num > 1)
                index = ceil(num*rand);
                bestMove = bestMoves(index, :);
            else 
                bestMove = bestMoves; % If only one best move
            end

            % If there is no possible move...
            if (changed == false)
                bestMove = [99 99];
            end
        %else
            % Outputs if it is not this player's turn
        %end
    end

end