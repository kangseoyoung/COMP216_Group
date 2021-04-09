import group_5_publisher as pub

pub1 = pub.publisher(max_msg=2)
pub2 = pub.publisher(max_msg=2)

pub1.send_data()
print("==========")
pub2.send_data()