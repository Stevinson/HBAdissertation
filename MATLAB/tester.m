% Run a series of simulations with given agents
% Edward Stevinson 15/7/16
%%
import othello_scripts.*
    
%% Initialise   
state = getNewboard(); % Creates a board with initial disks on

%% Types
% Define the classes of types the HBA agent will use in the simulation.
M = {
    H1_maximum_disk(), simple_agent_workspace();
    H2_maximum_value(), simple_agent_workspace();
    };

%% Agents
% Define the agents playing the simulation.
% A{i,1} contains a pointer to agent i's algorithm
% A{i,2} contains the initial workspace of agent i's algorithm.
A = {
    % What will eventually go here are agents that mix a certain way over the types, not the pure types themselves.
    H2_maximum_value(), simple_agent_workspace(); % Non HBA-agent
    H1_maximum_disk(), simple_agent_workspace(); % Non HBA-agent
    %HBA_agent(5,5,@transition), HBA_agent_workspace(M, sum_likelihood(1),'UNIFORM'); % HBA-agent
    };

%% Maximum of 1000 transitions
max_transitions = 1000;
state.turn = 1; % i.e. black moves first
state.opponent = 2; % i.e. white goes second
state.wins = 0; state.plays = 0; state.end = false; state.children = 0;


%% Optional extras
options = struct('plot', @plotBoard);

%% Run simulation
state = simulate_othello(A, @tran, state, max_transitions, options);
fprintf('game has ended');
fprintf('score was:' );

score = getScore(state);
% Black score
black_score = score(1,1)
% White score
white_score = score(1,2)


