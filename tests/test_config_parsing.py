import unittest
import yaml
from pathlib import Path

class TestConfigParsing(unittest.TestCase):
    def setUp(self):
        with open('config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

    def test_video_dimensions(self):
        video = self.config['dimensions']['video']
        self.assertEqual(len(video), 2)
        self.assertIsInstance(video[0], int)  # x
        self.assertIsInstance(video[1], int)  # y

    def test_signal_dimensions(self):
        signal = self.config['dimensions']['signal']
        self.assertEqual(len(signal), 2)
        self.assertIsInstance(signal[0], int)  # x
        self.assertIsInstance(signal[1], int)  # y

    def test_arena_dimensions(self):
        arena = self.config['dimensions']['arena']
        self.assertEqual(len(arena), 4)
        self.assertIsInstance(arena[0], int)  # left
        self.assertIsInstance(arena[1], int)  # top
        self.assertIsInstance(arena[2], int)  # right
        self.assertIsInstance(arena[3], int)  # bottom

    def test_exit_dimensions(self):
        exit = self.config['dimensions']['exit']
        self.assertEqual(len(exit), 4)
        self.assertIsInstance(exit[0], int)  # left
        self.assertIsInstance(exit[1], int)  # top
        self.assertIsInstance(exit[2], int)  # right
        self.assertIsInstance(exit[3], int)  # bottom

    def test_video_config(self):
        video = self.config['video']
        self.assertIn('fps', video)
        self.assertIn('thumbnail_scale', video)
        self.assertIsInstance(video['fps'], int)
        self.assertIsInstance(video['thumbnail_scale'], float)

    def test_tracking_config(self):
        tracking = self.config['tracking']
        self.assertIn('target_bodypart', tracking)
        self.assertIn('background_image', tracking)
        self.assertIn('pcutoff', tracking)
        self.assertIn('event', tracking)
        self.assertIn('min_escape_frames', tracking)
        self.assertIn('max_escape_window', tracking)
        self.assertIn('speed_cutoff', tracking)
        self.assertIsInstance(tracking['target_bodypart'], str)
        self.assertIsInstance(tracking['background_image'], str)
        self.assertIsInstance(tracking['pcutoff'], float)
        self.assertIsInstance(tracking['min_escape_frames'], int)
        self.assertIsInstance(tracking['max_escape_window'], int)
        self.assertIsInstance(tracking['speed_cutoff'], int)
        self.assertTrue(Path(tracking['background_image']).is_file())
        
    def test_signal_config(self):
        signal = self.config['signal']
        self.assertIn('threshold', signal)
        self.assertIn('start_frame', signal)
        self.assertIn('end_frame', signal)
        self.assertIsInstance(signal['threshold'], int)
        self.assertIsInstance(signal['start_frame'], int)
        self.assertIsInstance(signal['end_frame'], int)

if __name__ == '__main__':
    unittest.main(verbosity=2)

