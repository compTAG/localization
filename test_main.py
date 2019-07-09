import Classes.test_cases as test_cases
import Classes.PCPDS as pcpds_util
import pptk

# test_obj = pcpds_util.PCPDS(1000)
# test_obj.set_point_cloud()
# # Try saving the object
# test_obj.save("/home/geoengel/Documents/Undergraduate Research/localization/Sections/")

pcpds = pcpds_util.load_section_dir("/home/geoengel/Documents/Undergraduate Research/localization/Sections/test_2_2019-07-09", "1011")

point_cloud = pcpds.get_point_cloud()

print("\nSection Point_Cloud Point total:", len(pcpds.get_point_cloud()))

print("Point output:\n", pcpds.get_point_cloud())

print("\nPoint Selection Test:\n", pcpds.get_point_cloud()[0])

print("\nPoint X Selection Test:\n", pcpds.get_point_cloud()[0][0])

v = pptk.viewer(point_cloud)
v.set(point_size=0.01)

#test_cases.rotate_section_z(pcpds, 90) 