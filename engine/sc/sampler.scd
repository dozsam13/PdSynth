s.boot;
~bs = SoundFile.collectIntoBuffers("C:/dev/PdSynth/samples/emx-sample-pack-50tube/*");
~bs[0].path;
~bs[0].bufnum;


/*
(
var sample_datas;
var app_osc_client;

sample_datas = ~bs.collect({|b| [b.path.basename, b.bufnum]});
app_osc_client = NetAddr.new("127.0.0.1", 57121);
sample_datas.asString.postln;
app_osc_client.sendMsg("/test", sample_datas.asString);
)
*/
(
SynthDef.new(\sampy, {
	var sig, env;

	sig = PlayBuf.ar(
		numChannels: 2,
		bufnum: \buf.kr(0),
		rate: BufRateScale.kr(\buf.kr(0)) * \rate.kr(1),  //44100/44100
		startPos: \spos.kr(0)
	);
	env = EnvGen.kr(
		envelope: Env(
			levels: [0, 1, 0],
			times:[\atk.ir(0.01), \decay.ir(0.5)],
			curve: [0, 0]
		),
		doneAction: 2
	);
	Out.ar(\out.kr(0), sig*env*\amp.kr(1));
}).add;
)

(
t = TempoClock.new(200/60).permanent_(true);
~postBeat = {t.beats.postln;1;};
t.schedAbs(t.nextBar, {~postBear.value});
)
t.beats.postln;
t.stop;


(
~track_ids = [1, 2];
~paramDict = Dictionary();
~patterns = [];
/*~paramDict.put(\amp_1, 1.0);
~paramDict.put(\bufnum_1, ~bs[14].bufnum);
~paramDict.put(\rate_1, Pseq([1.0], 1));
~paramDict.put(\freq_1, Pseq([100, \, \, \], 1));
*/
~track_ids.do({
	arg track_id;

	~paramDict.put(("amp_" ++ track_id).asSymbol, 1.0);
	~paramDict.put(("bufnum_" ++ track_id).asSymbol, ~bs[14].bufnum);
	~paramDict.put(("rate_" ++ track_id).asSymbol, Pseq([1.0], 1));
	~paramDict.put(("freq_" ++ track_id).asSymbol, Pseq([100, \, \, \], 1));
});
/*
~paramDict.put(\amp_2, 1.0);
~paramDict.put(\bufnum_2, ~bs[63].bufnum);
~paramDict.put(\rate_2, Pseq([1.0], 1));
~paramDict.put(\freq_2, Pseq([\, \, 100, \], 1));
*/
)


(
~patterns = ~track_ids.collect{
	arg track_id;

	// Create OSC param bindings
	OSCdef(("amp_" ++ track_id).asSymbol, { |msg|
		//msg[1].postln;
		~paramDict[("amp_" ++ track_id).asSymbol] = msg[1];
	}, "/amp_" ++ track_id);

	OSCdef(("bufnum_" ++ track_id).asSymbol, { |msg|
		//msg[1].postln;
		~paramDict[("bufnum_" ++ track_id).asSymbol] = msg[1];
	}, "/bufnum_" ++ track_id);

	OSCdef(("rate_" ++ track_id).asSymbol, { |msg|
		//msg[1].postln;
		~paramDict[("rate_" ++ track_id).asSymbol] = Pseq([msg[1]], 1);
	}, "/rate_" ++ track_id);

	OSCdef(("freq_" ++ track_id).asSymbol, { |msg|
		var seq, s2;
		seq = msg.drop(1);
		seq.postln;
		~paramDict[("freq_" ++ track_id).asSymbol] = Pseq(seq, 1);
	}, "/freq_" ++ track_id);


	// Create Pattern for track
	Pbind(
		\instrument, \sampy,
		\dur, 0.25,
		\amp, Pfunc({~paramDict[("amp_" ++ track_id).asSymbol]}),
		\buf, Pfunc({~paramDict[("bufnum_" ++ track_id).asSymbol]}),
		\rate, Pn(Plazy({~paramDict[("rate_" ++ track_id).asSymbol]}), inf),
		\freq, Pn(Plazy({~paramDict[("freq_" ++ track_id).asSymbol]}), inf)
	);

}
)

(
OSCdef(\start_seq, { |msg|
	~players = ~patterns.collect({ |ptn|
		ptn.play(t)
	});

}, "/start_seq");

OSCdef(\stop_seq, { |msg|
	~players.do({ |player|
		player.stop;
	});
}, "/stop_seq");

OSCdef(\bpm, { |msg|
	t.tempo = msg[1]/60;
}, "/bpm");

OSCdef(\volume, { |msg|
	s.volume.volume = if(msg[1] > 1) {1} {msg[1]};
}, "/volume");
)


(
~plr1 = ~patterns[0].play(t);
~plr2 = ~patterns[1].play(t);
)

(
~plr1.stop;
~plr2.stop;
)

~paramDict[\freq_1] = Pseq([100, \, \, \], 1);
~paramDict[\freq_2] = Pseq([\, \, 100, \], 1);

~paramDict[\amp_1] = 1.0;
~paramDict[\amp_2] = 0.7;
~paramDict[\rate_1] = Pseq([1.0], 1);
~paramDict[\rate_2] = Pseq([1.0], 1);
~paramDict[\freq_1] = Pseq([0, \, \, \], 1);
~patterns.size.postln;


s.freeAll;
