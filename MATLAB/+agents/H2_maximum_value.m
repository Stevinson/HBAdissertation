%%
% Maximum value type - ie agents rank different squares by preference and 
% always choose certain squares over other.
%
% Edward Stevinson 4/8/16
%%

function f = H2_maximum_value()

    %import othello.scripts.*
    f = @heuristic;

    function [bestMove, possibleMoves, W] = heuristic(i,~,board,~,W,~)
        
        import othello_scripts.*
       
        % Initialise
        possibleMoves = [];
        bestMove = [99, 99]; % Initialise to 99 for error checking
        
        % Hashmap values for each different square
        squares = {'[1 1]','[1 8]','[8 1]','[8 8]','[2 2]','[2 7]','[7 2]','[7 7]','[1 2]','[1 7]','[2 1]','[2 8]','[7 1]','[7 8]','[8 2]','[8 7]',...
            '[1 3]','[1 4]','[1 5]','[1 6]','[8 3]','[8 4]','[8 5]','[8 6]','[3 1]','[4 1]','[5 1]','[6 1]','[3 8]','[4 8]','[5 8]','[6 8]'};

        values = [2,2,2,2,-2,-2,-2,-2,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1];
        mapObj = containers.Map(squares, values);
        
        % Get possible moves 
        possibleMoves = othello_scripts.getValidMoves(board, i);
        numberMoves = size(possibleMoves,1);
        moveValues = zeros(size(possibleMoves,1),1);
    
        for j = 1:numberMoves
           
            % Convert possible move coordinate into a string for use in hashmap
            coord = mat2str(possibleMoves(j,:));
            
            if (isKey(mapObj, coord))
            
                if (mapObj(coord) == 2)
                
                    moveValues(j) = 2;
                
                elseif (mapObj(coord) == 1)
                    
                    moveValues(j) = 1;
                
                elseif (mapObj(coord) == -1)
                    
                    moveValues(j) = -1;
                
                else %(mapObj(coord) == -2)
                    
                    moveValues(j) = -2;
                
                end
                    
            else
                
                moveValues(j) = 0;
                
            end
   
        end
        
        % Randomly select best move from all moves that give the highest square value
        if (numel(possibleMoves)>0)
            maxValue = max(moveValues);
            indices = find(moveValues == maxValue);
            index = indices(randi(numel(indices)));
            bestMove = possibleMoves(index,:);
        else
            bestMove = [99,99];
        end
    end
end

 