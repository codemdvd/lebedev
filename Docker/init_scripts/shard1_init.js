rs.initiate(
    {
        _id: "shard1rs",
        members: [
            { _id: 0, host: 'shard1svr1' },
            { _id: 1, host: 'shard1svr2' },
        ]
    }
);