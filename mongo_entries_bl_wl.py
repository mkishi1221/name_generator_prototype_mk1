from classes.user_repository.mutations.user_cache import UserCacheMutations
from classes.user_repository.mutations.user_preferences import UserPreferenceMutations
from classes.user_repository.repository import UserRepository

UserRepository.init_user()
print("black list:")
print(UserPreferenceMutations.get_blacklisted())
print("white list:")
print(UserPreferenceMutations.get_whitelisted())
print("short list:")
print(UserPreferenceMutations.get_shortlisted())
