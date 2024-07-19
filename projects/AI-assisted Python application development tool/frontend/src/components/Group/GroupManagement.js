
// Group management component
// Handles group settings and member management

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GroupManagement = ({ groupId }) => {
  const [groupName, setGroupName] = useState('');
  const [members, setMembers] = useState([]);
  const [newMember, setNewMember] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchGroupDetails();
  }, [groupId]);

  const fetchGroupDetails = async () => {
    try {
      const response = await axios.get(`/api/groups/${groupId}`);
      setGroupName(response.data.name);
      setMembers(response.data.members);
    } catch (err) {
      console.error('Error fetching group details:', err);
      setError('Failed to fetch group details');
    }
  };

  const updateGroupName = async () => {
    try {
      await axios.put(`/api/groups/${groupId}`, { name: groupName });
      setError('');
    } catch (err) {
      console.error('Error updating group name:', err);
      setError('Failed to update group name');
    }
  };

  const addMember = async () => {
    try {
      const response = await axios.post(`/api/groups/${groupId}/members`, { username: newMember });
      setMembers([...members, response.data]);
      setNewMember('');
      setError('');
    } catch (err) {
      console.error('Error adding member:', err);
      setError('Failed to add member');
    }
  };

  const removeMember = async (memberId) => {
    try {
      await axios.delete(`/api/groups/${groupId}/members/${memberId}`);
      setMembers(members.filter(member => member.id !== memberId));
      setError('');
    } catch (err) {
      console.error('Error removing member:', err);
      setError('Failed to remove member');
    }
  };

  if (process.env.NODE_ENV === 'development') {
    console.log('Group Management Component Rendered');
    console.log('Group ID:', groupId);
    console.log('Group Name:', groupName);
    console.log('Members:', members);
  }

  return (
    <div className="group-management">
      <h2>Group Management</h2>
      {error && <p className="error">{error}</p>}
      <div>
        <input
          type="text"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
          placeholder="Group Name"
        />
        <button onClick={updateGroupName}>Update Name</button>
      </div>
      <div>
        <h3>Members</h3>
        <ul>
          {members.map((member) => (
            <li key={member.id}>
              {member.username}
              <button onClick={() => removeMember(member.id)}>Remove</button>
            </li>
          ))}
        </ul>
      </div>
      <div>
        <input
          type="text"
          value={newMember}
          onChange={(e) => setNewMember(e.target.value)}
          placeholder="New Member Username"
        />
        <button onClick={addMember}>Add Member</button>
      </div>
    </div>
  );
};

export default GroupManagement;
