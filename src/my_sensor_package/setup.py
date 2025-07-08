# from setuptools import find_packages, setup

# package_name = 'my_sensor_package'

# setup(
#     name=package_name,
#     version='0.0.0',
#     packages=find_packages(exclude=['test']),
#     data_files=[
#         ('share/ament_index/resource_index/packages',
#             ['resource/' + package_name]),
#         ('share/' + package_name, ['package.xml']),
#     ],
#     install_requires=['setuptools'],
#     zip_safe=True,
#     maintainer='root',
#     maintainer_email='root@todo.todo',
#     description='TODO: Package description',
#     license='TODO: License declaration',
#     tests_require=['pytest'],
#     entry_points={
#         'console_scripts': [
#             "sensor_publisher_node = my_sensor_package.sensor_publisher:main",
#             "sensor_subscriber_node = my_sensor_package.sensor_subscriber:main",
        
#         ],
#     },
# )

import os
from glob import glob
from setuptools import setup

package_name = 'my_sensor_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yeml]'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name', 
    maintainer_email='your_email@example.com', 
    description='Beginner ROS2 package for sensor simulation',
    license='Apache License 2.0', 
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "sensor_publisher_node = my_sensor_package.sensor_publisher:main",
             "sensor_subscriber_node = my_sensor_package.sensor_subscriber:main",
        ],
    },
)
