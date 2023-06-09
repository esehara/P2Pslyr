import libtorrent as lt
import time


class Client():

    def download(self, torrent_path, save_path):
        """
        torrentファイルを読み込み、本体ファイルをダウンロードする。

        Parameters
        ----------
        torrent_path : str
        ダウンロードを行うtorrentファイルへのパス。
        save_path : str
        実ファイルのダウンロード先のパス。
        """

        session = lt.session({'listen_interfaces': '0.0.0.0:6881'})

        info = lt.torrent_info(torrent_path)
        handle = session.add_torrent({'ti': info, 'save_path': save_path})

        print('starting', handle.status().name)

        while not handle.status().is_seeding:
            s = handle.status()

            peer_info = handle.get_peer_info()

            print("downloading: %.2f%% complete (down: %.1f kB/s, up: %.1f kB/s, peers: %d) %s" % (
                s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                len(peer_info), s.state))

            for p in peer_info:
                print("IP address: %s   Port: %d" % (p.ip[0], p.ip[1]))

            time.sleep(1)

        print(handle.status().name, 'complete')
