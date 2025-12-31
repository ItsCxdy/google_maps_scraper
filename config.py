"""
Configuration Module

This module handles all configuration settings for the Google Maps scraper,
including API keys, default search parameters, and other configurable options.
"""

import os
from typing import Dict, Any


class Config:
    """Configuration class for Google Maps scraper settings."""
    
    def __init__(self):
        """Initialize configuration with default values."""
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')
        self.default_location = 'United States'
        self.default_search_radius = 5000  # meters
        self.max_results = 20
        self.delay_between_requests = 1  # seconds
        self.timeout = 30  # seconds
        self.output_format = 'excel'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
    def get_api_key(self) -> str:
        """Get the Google Maps API key."""
        return self.api_key
    
    def get_default_location(self) -> str:
        """Get the default search location."""
        return self.default_location
    
    def get_default_search_radius(self) -> int:
        """Get the default search radius in meters."""
        return self.default_search_radius
    
    def get_max_results(self) -> int:
        """Get the maximum number of results to return."""
        return self.max_results
    
    def get_delay_between_requests(self) -> int:
        """Get the delay between requests in seconds."""
        return self.delay_between_requests
    
    def get_timeout(self) -> int:
        """Get the request timeout in seconds."""
        return self.timeout
    
    def get_output_format(self) -> str:
        """Get the output format for results."""
        return self.output_format
    
    def get_user_agent(self) -> str:
        """Get the user agent string for requests."""
        return self.user_agent
    
    def update_config(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration with provided dictionary."""
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'api_key': self.api_key,
            'default_location': self.default_location,
            'default_search_radius': self.default_search_radius,
            'max_results': self.max_results,
            'delay_between_requests': self.delay_between_requests,
            'timeout': self.timeout,
            'output_format': self.output_format,
            'user_agent': self.user_agent
        }