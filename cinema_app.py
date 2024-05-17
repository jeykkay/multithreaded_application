import threading


class Cinema:
    def __init__(self):
        self.movies = {'Movie1':
                           {'screening1': [True, True, True],
                            'screening2': [True, True, True]},
                       'Movie2':
                           {'screening1': [True, True, True],
                            'screening2': [True, True, True]}}

        self.lock = threading.Lock()
        self.available_seats = threading.Condition(self.lock)
        self.max_seats = 3
        self.reserved_threads = 0

    def reserve_seat(self, movie, screening, seats):
        with self.lock:
            if all(self.movies[movie][screening][seat] for seat in seats):
                for seat in seats:
                    self.movies[movie][screening][seat] = False

                print(f"Seats {seats} for {movie} at {screening} reserve successfully")
            else:
                print(f"Seats {seats} for {movie} at {screening} are already reserve")

            self.reserved_threads += 1

            if self.reserved_threads == 5:
                self.available_seats.notify_all()

    def print_status(self, movie, screening):
        with self.lock:
            while self.reserved_threads < 5:
                self.available_seats.wait()
            print(f"Seats status for {movie} at {screening}: {self.movies[movie][screening]}")


def custom_user(cinema, movie, screening, seats):
    cinema.reserve_seat(movie, screening, seats)


cinema = Cinema()

threads = []
for _ in range(5):
    thread = threading.Thread(target=custom_user, args=(cinema, "Movie1", "screening1", [0, 1, 2]))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

cinema.print_status("Movie1", "screening1")
