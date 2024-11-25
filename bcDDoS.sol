// SPDX-License-Identifier: MIT
pragma solidity ^0.5.5;

contract DDoSIncidentLogger 
{
    // Struct to store simplified incident information
    struct AttackInfo 
    {
        string targetIP;              // Targeted system/application
        string attackerIP;            // Source of the attack
        uint packetCount;             // Total packet count
        uint bandwidthImpact;         // Total bandwidth consumed (bytes)
        string attackType;            // Type of attack (e.g., UDP Flood)
        string attackPattern;         // Pattern of the attack (e.g., increasing)
        uint256 detectionStartTime;   // Start time of attack detection
        uint256 detectionEndTime;     // End time of attack detection
    }

    // Array to store each attack entry
    AttackInfo[] public attacks;

    // Function to log a new attack entry
    function logAttack
    (
        string memory _targetIP,
        string memory _attackerIP,
        uint _packetCount,
        uint _bandwidthImpact,
        string memory _attackType,
        string memory _attackPattern,
        uint256 _detectionStartTime,
        uint256 _detectionEndTime
    ) public {
        // Create and store the attack entry
        AttackInfo memory newAttack = AttackInfo(
            _targetIP,
            _attackerIP,
            _packetCount,
            _bandwidthImpact,
            _attackType,
            _attackPattern,
            _detectionStartTime,
            _detectionEndTime
        );
        attacks.push(newAttack);
    }

    // Retrieve a specific attack entry by index
    function getAttack(uint index) public view returns (
        string memory, string memory, uint, uint, string memory, string memory, uint256, uint256
    ) 
    {
        require(index < attacks.length, "Index out of bounds");
        AttackInfo memory attack = attacks[index];
        return (
            attack.targetIP,
            attack.attackerIP,
            attack.packetCount,
            attack.bandwidthImpact,
            attack.attackType,
            attack.attackPattern,
            attack.detectionStartTime,
            attack.detectionEndTime
        );
    }

    // Get the total number of attacks logged
    function getAttackCount() public view returns (uint) {
        return attacks.length;
    }
}

