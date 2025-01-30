# Translation layer for converting UptimeRobot API responses into the UptimeMatrix JSON format.
# Developed by Layeredy Software, a organization by Auri (auri.lol)
# Licensed under the MIT license, see LICENSE for more details.
# Copyright (c) 2025 Auri (projects@auri.lol)
# Designed for https://uptimerobot.com to work with https://uptimematrix.com | Documentation can be found at https://lyrdy.co/dko4
# Developed with the help of Copilot. 

import os
import requests
import json
from dotenv import load_dotenv
from typing import Dict, List, Any

load_dotenv()

class UptimeRobotConverter:
   def __init__(self):
       self.api_key = os.getenv('UPTIMEROBOT_API_KEY')
       self.api_url = 'https://api.uptimerobot.com/v2/getMonitors'
       self.excluded_monitors = self._load_excludes()
       
   def _load_excludes(self) -> List[str]:
       try:
           with open('excludes.json', 'r', encoding='utf-8') as f:
               data = json.load(f)
               return data.get('excluded_monitors', [])
       except FileNotFoundError:
           return []
       except json.JSONDecodeError:
           return []

   def _load_existing_data(self) -> Dict[str, Any]:
       try:
           with open('status.json', 'r', encoding='utf-8') as f:
               return json.load(f)
       except (FileNotFoundError, json.JSONDecodeError):
           return {}

   def get_monitors(self) -> Dict[str, Any]:
       headers = {
           'content-type': 'application/x-www-form-urlencoded',
           'cache-control': 'no-cache'
       }
       
       payload = {
           'api_key': self.api_key,
           'format': 'json',
           'logs': '1',
           'custom_uptime_ratios': '1-7-30-365',
           'response_times': '1'
       }
       
       response = requests.post(self.api_url, headers=headers, data=payload)
       response.raise_for_status()
       return response.json()

   def convert_status(self, status: int) -> str:
       status_map = {
           0: 'Unknown',
           1: 'Operational',
           2: 'Operational',
           8: 'Degraded',
           9: 'Issue'
       }
       return status_map.get(status, 'Unknown')

   def parse_monitor_tags(self, monitor: Dict) -> List[str]:
       friendly_name = monitor.get('friendly_name', '')
       
       if '[' in friendly_name and ']' in friendly_name:
           start = friendly_name.find('[')
           end = friendly_name.find(']')
           tags_str = friendly_name[start + 1:end]
           return [tag.strip() for tag in tags_str.split(',') if tag.strip()]
       
       return []

   def clean_monitor_name(self, name: str) -> str:
       if '[' in name and ']' in name:
           return name[:name.find('[')].strip()
       return name.strip()

   def group_monitors_by_category(self, monitors: List[Dict]) -> List[Dict]:
       categories = {}
       
       for monitor in monitors:
           clean_name = self.clean_monitor_name(monitor.get('friendly_name', ''))
           
           if clean_name in self.excluded_monitors:
               continue
               
           tags = self.parse_monitor_tags(monitor)
           
           if not tags:
               if "Ungrouped" not in categories:
                   categories["Ungrouped"] = []
               categories["Ungrouped"].append({
                   'serviceName': clean_name,
                   'status': self.convert_status(monitor.get('status'))
               })
               continue
           
           for tag in tags:
               if tag not in categories:
                   categories[tag] = []
               
               categories[tag].append({
                   'serviceName': clean_name,
                   'status': self.convert_status(monitor.get('status'))
               })
       
       return [
           {
               'categoryName': category,
               'services': sorted(services, key=lambda x: x['serviceName'])
           }
           for category, services in sorted(categories.items())
       ]

   def get_formatted_data(self) -> Dict[str, Any]:
       monitors_data = self.get_monitors()
       existing_data = self._load_existing_data()
       
       default_data = {
           'OverallStatus': 'NoOverride',
           'RandomOperationalMessage': True,
           'Whitelabel': False,
           'announcement': {
               'text': ''
           },
           'maintenanceAlerts': [],
           'sections': {
               'announcementBar': False,
               'maintenanceAlerts': False,
               'statusUpdates': False
           },
           'statusUpdates': []
       }

       formatted_data = {**default_data, **existing_data}
       formatted_data['services'] = self.group_monitors_by_category(monitors_data.get('monitors', []))
       formatted_data['RandomOperationalMessage'] = True
       
       return formatted_data

def main():
   converter = UptimeRobotConverter()
   
   try:
       formatted_data = converter.get_formatted_data()
       
       with open('status.json', 'w', encoding='utf-8') as f:
           json.dump(formatted_data, f, indent=2)
           
   except Exception as e:
       print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
   main()