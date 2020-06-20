class server():
	sock
	new_rooms
	rooms

	def server_handler():
		while True:
			select(sock)
			if sock:
				thread(client_handler)
			if new_rooms:
				for room in new_rooms:
					move_room()
					thread(room_handler)

	def client handler():
		shimi = Clinet (a,b,c)
		if(new_room)
			self.new_rooms.add(create_room)
		else:
			join_room()


class room():
	room_handler():
		while True:
			select(socks)
		if sock:
			send_to_all()

