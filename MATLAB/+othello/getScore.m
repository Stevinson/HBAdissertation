% Get the score of the current game
% Edward Stevinson 18/7/16
%%

function [score, winner] = getScore(state)

    black_score = 0;
    white_score = 0;
    for x = 1:8 
        for y = 1:8
            if (state.positions(x,y) == 1)
                black_score = black_score + 1;
            end
            if (state.positions(x,y) == 2)
                white_score = white_score + 1;
            end
        end
    end
    score = [black_score, white_score];
    
    % Variable that returns who was the winner, black or white?
    if (black_score > white_score)
        winner = 1;
    elseif (black_score < white_score)
        winner = 2;
    else
        winner = 0;
    end

end