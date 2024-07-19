
// frontend/src/components/Search/Search.js
// Purpose: Advanced search component for the secure messaging platform
// Description: Provides functionality for searching messages, contacts, and groups

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Search = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState('messages');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (searchQuery.length > 2) {
      performSearch();
    } else {
      setSearchResults([]);
    }
  }, [searchQuery, searchType]);

  const performSearch = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.get('/api/search', {
        params: {
          query: searchQuery,
          type: searchType
        },
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      setSearchResults(response.data.results);
    } catch (err) {
      console.error('Search error:', err);
      setError('An error occurred while searching. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSearchTypeChange = (e) => {
    setSearchType(e.target.value);
  };

  const renderSearchResults = () => {
    if (isLoading) {
      return <p>Loading...</p>;
    }

    if (error) {
      return <p className="error">{error}</p>;
    }

    if (searchResults.length === 0) {
      return <p>No results found.</p>;
    }

    return (
      <ul className="search-results">
        {searchResults.map((result) => (
          <li key={result.id} className="search-result-item">
            {searchType === 'messages' && (
              <div>
                <p>{result.content}</p>
                <small>From: {result.sender} - {new Date(result.timestamp).toLocaleString()}</small>
              </div>
            )}
            {searchType === 'contacts' && (
              <div>
                <p>{result.name}</p>
                <small>{result.email}</small>
              </div>
            )}
            {searchType === 'groups' && (
              <div>
                <p>{result.name}</p>
                <small>Members: {result.memberCount}</small>
              </div>
            )}
          </li>
        ))}
      </ul>
    );
  };

  return (
    <div className="search-component">
      <h2>Advanced Search</h2>
      <div className="search-controls">
        <input
          type="text"
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Enter search query"
          className="search-input"
        />
        <select value={searchType} onChange={handleSearchTypeChange} className="search-type-select">
          <option value="messages">Messages</option>
          <option value="contacts">Contacts</option>
          <option value="groups">Groups</option>
        </select>
      </div>
      {renderSearchResults()}
    </div>
  );
};

export default Search;
