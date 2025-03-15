s.boot;
~bs = SoundFile.collectIntoBuffers("C:/dev/PdSynth/samples/emx-sample-pack-50tube/*");

SynthDef(\sampy, {
	arg buf, rate=1, amp=1, attackTime = 0.0, decayTime = 0.3, sustainLevel = 0.5, releaseTime = 1.0;
	var sig, env, envgen;
	sig = SinOsc.ar(470); //PlayBuf.ar(1, buf, rate, \t_tr.kr(1, 0) );
	env = EnvGen.ar(Env.adsr(attackTime, decayTime, sustainLevel, releaseTime);, doneAction: Done.freeSelf);
	Out.ar([0,1], sig*amp*env);
}).add;

var sustain_level = 0.5;
a = Synth(\sampy, [\buf, ~bs[14].bufnum]);
a.free;

a.set(\buf, ~bs[14].bufnum, \t_tr, 1, \attackTime, 0.0);
a.set(\buf, ~bs[14].bufnum, \t_tr, 1, \attackTime, 10.0);

p = Pbind(
	\instrument, \sampy
).play;

s.plotTree;
p.stop;

b = (
{
    var env = Env.adsr(0.5, 0.5, 0.5, 1.0);
    SinOsc.ar(470) * EnvGen.kr(env, doneAction: Done.freeSelf)
}.play
)

b.stop;