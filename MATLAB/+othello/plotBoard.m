% Plotter for othello game
% Inputs:
%     state: current game state
%%

function plotBoard(state)
    
    % Check if there is a desired figure number
    if nargin < 2, fn = 1; end
   
    % Drawing board background
    axis off
    axis([0.5 8.5 0.5 8.5])
    for i=1:8
        for j=1:8
            rectangle('Position',[i-0.5,j-0.5,1,1],'FaceColor','g')
        end
    end
    
    % Draw black pieces
    [row,col] = find(state.positions==1);
    if ~isempty(row)
        for i=1:1:numel(row)
            rectangle('Position',[col(i)-0.3,8.7-row(i),0.6,0.6],'Curvature',[1 1],'FaceColor','k')
        end
    end
    
    % Draw white pieces
    [row,col] = find(state.positions==2);
    if ~isempty(row)
        for i=1:1:numel(row)
            rectangle('Position',[col(i)-0.3,8.7-row(i),0.6,0.6],'Curvature',[1 1],'FaceColor','w')
        end
    end
    
end