% Function that takes in a coordinate and returns true if it is on the
% othello board
% Edward Stevinson 16/7/16
%%

function ans = isOnBoard(x, y)

    if (x >= 1) && (x <= 8) && (y >= 1) && (y <= 8)
        ans = true;
    else
        ans = false;
    end
    
end

