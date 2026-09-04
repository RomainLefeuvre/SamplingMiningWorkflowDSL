import requests
import json
import time
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SWHGraphAPIClient:


    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        # Timeout pour éviter les blocages
        self.session.timeout = 30
        self.latest_commit_dates_cache: Dict[int, Optional[int]] = {}
        self.commit_counts_cache: Dict[int, Optional[int]] = {}
        self.committer_counts_cache: Dict[int, Optional[int]] = {}
        
    def health_check(self) -> bool:
        """Vérifie si l'API est disponible"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_all_origin_ids(self) -> List[int]:
        """Récupère tous les IDs d'origine"""
        try:
            response = self.session.get(f"{self.base_url}/origins")
            response.raise_for_status()
            data = response.json()
            return data.get('origin_ids', [])
        except Exception as e:
            logger.error(f"Failed to get origin IDs: {e}")
            return []
    
    def cache_latest_commit_dates(self):
        """Récupère les dates des derniers commits pour toutes les origines"""
        try:
            response = self.session.get(f"{self.base_url}/origins/latest-commit-dates")
            response.raise_for_status()
            data = response.json()
            #Convert key and values to int
            data = {int(k): int(v) for k, v in data.items()}
            self.latest_commit_dates_cache = data
           
        except Exception as e:
            logger.error(f"Failed to get latest commit dates: {e}")

    def cache_commit_counts(self):
        """Récupère les compteurs de commits pour toutes les origines"""
        try:
            response = self.session.get(f"{self.base_url}/origins/commit-counts")
            response.raise_for_status()
            data = response.json()
            #Convert key and values to int
            data = {int(k): int(v) if v is not None else None for k, v in data.items()}
            self.commit_counts_cache = data
           
        except Exception as e:
            logger.error(f"Failed to get commit counts: {e}")

    def cache_committer_counts(self):
        """Récupère les compteurs de commiters pour toutes les origines"""
        try:
            response = self.session.get(f"{self.base_url}/origins/committer-counts")
            response.raise_for_status()
            data = response.json()
            #Convert key and values to int
            data = {int(k): int(v) if v is not None else None for k, v in data.items()}
            self.committer_counts_cache = data
           
        except Exception as e:
            logger.error(f"Failed to get committer counts: {e}")
           

    def get_origin_url(self, origin_id: int) -> Optional[str]:
        """Récupère l'URL d'une origine"""
        try:
            response = self.session.get(f"{self.base_url}/origins/{origin_id}/url")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            return data.get('url')
        except Exception as e:
            logger.error(f"Failed to get URL for origin {origin_id}: {e}")
            return None
    
    def get_latest_commit_date(self, origin_id: int) -> Optional[int]:
        """Récupère la date du dernier commit"""
        if self.latest_commit_dates_cache and origin_id in self.latest_commit_dates_cache:
            return self.latest_commit_dates_cache[origin_id]
        try:
            response = self.session.get(f"{self.base_url}/origins/{origin_id}/latest-commit-date")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            return data.get('latest_commit_date')
        except Exception as e:
            logger.error(f"Failed to get latest commit date for origin {origin_id}: {e}")
            return None
    
    def get_committer_count(self, origin_id: int) -> Optional[int]:
        """Récupère le nombre de commiters"""
        if self.committer_counts_cache and origin_id in self.committer_counts_cache:
            return self.committer_counts_cache[origin_id]
        try:
            response = self.session.get(f"{self.base_url}/origins/{origin_id}/committer-count")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            return data.get('committer_count')
        except Exception as e:
            logger.error(f"Failed to get committer count for origin {origin_id}: {e}")
            return None
    
    def get_commit_count(self, origin_id: int) -> Optional[int]:
        """Récupère le nombre de commits"""
        if self.commit_counts_cache and origin_id in self.commit_counts_cache:
            return self.commit_counts_cache[origin_id]
        try:
            response = self.session.get(f"{self.base_url}/origins/{origin_id}/commit-count")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            return data.get('commit_count')
        except Exception as e:
            logger.error(f"Failed to get commit count for origin {origin_id}: {e}")
            return None
    
    def get_origin_complete_info(self, origin_id: int) -> Dict:
        """Récupère toutes les informations d'une origine"""
        logger.info(f"Getting complete info for origin {origin_id}")
        
        return {
            'id': origin_id,
            'url': self.get_origin_url(origin_id),
            'latest_commit_date': self.get_latest_commit_date(origin_id),
            'committer_count': self.get_committer_count(origin_id),
            'commit_count': self.get_commit_count(origin_id)
        }

def fetch_origin_info(client: SWHGraphAPIClient, origin_id: int) -> Dict:
    """Fonction pour récupérer les infos d'une origine (pour le parallélisme)"""
    return client.get_origin_complete_info(origin_id)

def main():
    # Initialisation du client
    client = SWHGraphAPIClient()
    
    # Vérification de la santé de l'API
    if not client.health_check():
        logger.error("API is not available!")
        return
    
    logger.info("API is healthy!")
    
    # Récupération de tous les IDs d'origine
    logger.info("Fetching all origin IDs...")
    origin_ids = client.get_all_origin_ids()
    
    if not origin_ids:
        logger.error("No origin IDs found!")
        return
    
    logger.info(f"Found {len(origin_ids)} origins")
    
    # Version séquentielle (plus lente mais plus simple)
    logger.info("=== Sequential processing ===")
    origins_data = []
    
    for i, origin_id in enumerate(origin_ids[:5]):  # Limité aux 5 premiers pour le test
        logger.info(f"Processing origin {i+1}/{len(origin_ids[:5])}: {origin_id}")
        origin_info = client.get_origin_complete_info(origin_id)
        origins_data.append(origin_info)
        
        # Affichage des résultats
        print(f"\nOrigin {origin_id}:")
        print(f"  URL: {origin_info['url']}")
        print(f"  Latest commit date: {origin_info['latest_commit_date']}")
        print(f"  Committer count: {origin_info['committer_count']}")
        print(f"  Commit count: {origin_info['commit_count']}")
    


if __name__ == "__main__":
    main()