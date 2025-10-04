import pytest
import yaml
from pathlib import Path
from src.weather_api.config.loader import Config


class TestConfig:
    def test_config_initialization(self):
        """Test that Config initializes correctly"""
        config = Config()
        assert config.config_dir is not None
        assert isinstance(config.config_dir, Path)

    def test_database_config_loaded(self):
        """Test that database config is loaded from YAML"""
        config = Config()
        assert config.database_config is not None
        assert isinstance(config.database_config, dict)

    def test_database_config_structure(self):
        """Test that database config has expected keys"""
        config = Config()
        assert 'host' in config.database_config
        assert 'port' in config.database_config
        assert 'dbname' in config.database_config

    def test_database_config_values(self):
        """Test that database config has expected values"""
        config = Config()
        assert config.database_config['host'] == 'postgres.weather.svc.cluster.local'
        assert config.database_config['port'] == '5432'
        assert config.database_config['dbname'] == 'weather_forecasts'

    def test_load_yaml_method(self):
        """Test that load_yaml method works correctly"""
        config = Config()
        yaml_path = config.config_dir / 'database.yaml'
        loaded_data = config.load_yaml(yaml_path)

        assert loaded_data is not None
        assert 'database' in loaded_data
        assert isinstance(loaded_data['database'], dict)
