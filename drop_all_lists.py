from classes.user_repository.repository import UserRepository
from classes.user_repository.mutations.user_preferences import UserPreferenceMutations
import os

try:
    os.remove("ref/logs/result_log.json")
except FileNotFoundError:
    print("result_log.json not found!")

UserRepository.init_user()
UserPreferenceMutations._drop_blacklist()
UserPreferenceMutations._drop_greylist()
UserPreferenceMutations._drop_whitelist()
UserPreferenceMutations._drop_shortlist()
