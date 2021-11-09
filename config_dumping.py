import os

for root, dirs, files in os.walk('./samples'):
    for path in files:
        path = os.path.join(root, path)
        file = os.system('DarkGroupConfigurationExtractor.exe {0}'.format(path))