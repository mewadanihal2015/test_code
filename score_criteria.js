// Game Score Calculator
// Version: 1.0

// Function to calculate the player's score based on various criteria
function calculateScore(timeTaken, accuracy, bonusPoints, penalties) {
    // Constants for weighting each factor
    const TIME_WEIGHT = 1.5;      // Weight for time taken (lower is better)
    const ACCURACY_WEIGHT = 2;   // Weight for accuracy (higher is better)
    const BONUS_WEIGHT = 1;      // Weight for bonus points (add directly)
    const PENALTY_WEIGHT = 2;    // Weight for penalties (subtract directly)

    // Score calculations
    const timeScore = Math.max(0, 100 - timeTaken * TIME_WEIGHT);
    const accuracyScore = accuracy * ACCURACY_WEIGHT;
    const bonusScore = bonusPoints * BONUS_WEIGHT;
    const penaltyScore = penalties * PENALTY_WEIGHT;

    // Total score
    const totalScore = Math.round(timeScore + accuracyScore + bonusScore - penaltyScore);

    // Ensure score is not negative
    return Math.max(0, totalScore);
}

// Function to generate a random player performance for demonstration
function randomGamePerformance() {
    const randomTime = Math.floor(Math.random() * 120) + 1; // Random time between 1 and 120 seconds
    const randomAccuracy = Math.random() * 100;            // Random accuracy percentage (0-100)
    const randomBonus = Math.floor(Math.random() * 50);    // Random bonus points (0-50)
    const randomPenalties = Math.floor(Math.random() * 20); // Random penalties (0-20)

    return { randomTime, randomAccuracy, randomBonus, randomPenalties };
}

// Simulate and display the results for 5 players
function simulateGame() {
    for (let i = 1; i <= 5; i++) {
        const { randomTime, randomAccuracy, randomBonus, randomPenalties } = randomGamePerformance();
        const score = calculateScore(randomTime, randomAccuracy, randomBonus, randomPenalties);

        console.log(`Player ${i}:`);
        console.log(`  Time Taken: ${randomTime} seconds`);
        console.log(`  Accuracy: ${randomAccuracy.toFixed(2)}%`);
        console.log(`  Bonus Points: ${randomBonus}`);
        console.log(`  Penalties: ${randomPenalties}`);
        console.log(`  Total Score: ${score}`);
        console.log('----------------------------------');
    }
}

// Run the simulation
simulateGame();

