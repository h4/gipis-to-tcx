import json


class Training(object):
    def __init__(self, filepath):
        self._load_from_json(filepath)

    def _load_from_json(self, filepath):
        f = open(filepath)
        self.data = json.loads(f.read())

    def get_all_data(self):
        return self.data

    @staticmethod
    def get_interval_range(base_speed):
        return base_speed * 0.9, base_speed * 1.1

    def get_workouts(self):
        return self.data.get(u'trainings', [])

    @staticmethod
    def _transform_workout(workout):
        if not u'segments' in workout:
            workout[u'segments'] = Training._create_segments(workout)

        workout[u'segments'] = map(Training._update_segment_speed, workout[u'segments'])

        return workout

    @staticmethod
    def _update_segment_speed(segment):
        value = segment.get(u'value')
        segment[u'value'] = map(Training._update_segment, value)
        return segment

    @staticmethod
    def _update_segment(segment):
        segment[u'speedMinMPS'], segment[u'speedMaxMPS'] = Training.get_interval_range(segment[u'speedMPS'])
        return segment

    @staticmethod
    def _create_segments(workout):
        return [{
                "reps": 1,
                "value": [{
                    "speedMPS": Training._get_workout_mps(workout),
                    "durationS": workout['durationS'],
                    "points": [],
                    "intensity": workout.get(u'intervalType', u''),
                }]
            }]

    @staticmethod
    def _get_workout_mps(workout):
        return workout[u'distanceM'] / workout[u'durationS']

    def convert(self):
        workouts = self.get_workouts()
        return map(self._transform_workout, workouts)
