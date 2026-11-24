import subprocess, sys
src, out = sys.argv[1], sys.argv[2]
dur=float(sys.argv[3]) if len(sys.argv)>3 else 4.5
d=[3]+[dur]*7; X=0.4
inp=[]
for i,dd in enumerate(d): inp+=['-loop','1','-t',str(dd),'-i',f'{src}/slide_{i+1}.png']
total=sum(d)-X*(len(d)-1)
subprocess.run(['python3','reel/music.py',f'{total:.2f}','reel/_m.wav'],check=True)
f=[f'[{i}:v]scale=1080:1920,format=yuv420p,fps=30[v{i}]' for i in range(len(d))]
prev='v0'; off=0
for i in range(1,len(d)):
    off+=d[i-1]-X; f.append(f'[{prev}][v{i}]xfade=transition=slideleft:duration={X}:offset={off:.2f}[x{i}]'); prev=f'x{i}'
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+['-i','reel/_m.wav','-filter_complex',';'.join(f),'-map',f'[{prev}]','-map',f'{len(d)}:a','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',out],check=True)
print(total)
